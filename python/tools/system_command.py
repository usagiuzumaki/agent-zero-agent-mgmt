"""
System command execution tool that bypasses sandboxing issues
"""
import subprocess
import os
import asyncio
from python.helpers.tool import Tool, Response

class SystemCommand(Tool):
    """Execute system commands directly without sandboxed sessions"""
    
    async def execute(self, **kwargs):
        """Run system commands reliably in deployed environments"""
        command = kwargs.get("command", "")
        timeout = kwargs.get("timeout", 60)
        working_dir = kwargs.get("working_dir", None)
        
        if not command:
            return Response(message="Please provide a command to execute", break_loop=False)
        
        try:
            # Prepare environment
            env = os.environ.copy()
            
            # For shell commands, we need to handle them properly
            if '|' in command or '>' in command or '&' in command:
                # Complex shell command - run through shell
                shell = True
                cmd = command
            else:
                # Simple command - can run directly
                shell = False
                cmd = command.split()
            
            # Execute command
            process = await asyncio.create_subprocess_shell(
                command if shell else " ".join(cmd),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=working_dir,
                env=env
            )
            
            # Wait for completion with timeout
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
                
                stdout_text = stdout.decode('utf-8', errors='replace') if stdout else ""
                stderr_text = stderr.decode('utf-8', errors='replace') if stderr else ""
                
                if process.returncode == 0:
                    message = f"✅ Command executed successfully\n\nOutput:\n{stdout_text}"
                    if stderr_text:
                        message += f"\n\nWarnings:\n{stderr_text}"
                else:
                    message = f"❌ Command failed with exit code {process.returncode}\n\nError:\n{stderr_text}"
                    if stdout_text:
                        message += f"\n\nOutput:\n{stdout_text}"
                
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                message = f"⏰ Command timed out after {timeout} seconds"
                
        except Exception as e:
            message = f"❌ Failed to execute command: {str(e)}"
        
        # Truncate very long output
        if len(message) > 5000:
            message = message[:5000] + "\n\n[Output truncated...]"
            
        return Response(message=message, break_loop=False)