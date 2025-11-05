"""
Improved code runner for deployed environments
Handles sandboxing issues and provides reliable execution
"""
import subprocess
import sys
import asyncio
import tempfile
import os
from typing import Tuple, Optional

class DeploymentCodeRunner:
    """Code runner optimized for deployed environments"""
    
    @staticmethod
    async def run_python_code(code: str, timeout: int = 30) -> Tuple[bool, str]:
        """Run Python code safely in deployed environment"""
        try:
            # Create a temporary file for the code
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Run the code in a subprocess
                process = await asyncio.create_subprocess_exec(
                    sys.executable, temp_file,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    env=os.environ.copy()
                )
                
                # Wait with timeout
                try:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(),
                        timeout=timeout
                    )
                    
                    stdout_text = stdout.decode('utf-8', errors='replace') if stdout else ""
                    stderr_text = stderr.decode('utf-8', errors='replace') if stderr else ""
                    
                    if process.returncode == 0:
                        return True, stdout_text
                    else:
                        return False, f"Error:\n{stderr_text}\nOutput:\n{stdout_text}"
                        
                except asyncio.TimeoutError:
                    process.kill()
                    await process.wait()
                    return False, f"Code execution timed out after {timeout} seconds"
                    
            finally:
                # Clean up temp file
                os.unlink(temp_file)
                
        except Exception as e:
            return False, f"Failed to run code: {str(e)}"
    
    @staticmethod
    async def run_shell_command(command: str, timeout: int = 30) -> Tuple[bool, str]:
        """Run shell commands safely in deployed environment"""
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=os.environ.copy()
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
                
                stdout_text = stdout.decode('utf-8', errors='replace') if stdout else ""
                stderr_text = stderr.decode('utf-8', errors='replace') if stderr else ""
                
                if process.returncode == 0:
                    return True, stdout_text
                else:
                    return False, f"Error:\n{stderr_text}\nOutput:\n{stdout_text}"
                    
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                return False, f"Command timed out after {timeout} seconds"
                
        except Exception as e:
            return False, f"Failed to run command: {str(e)}"
    
    @staticmethod 
    def can_import_package(package_name: str) -> bool:
        """Check if a package can be imported without hanging"""
        try:
            # Use subprocess to test import in isolation
            result = subprocess.run(
                [sys.executable, "-c", f"import {package_name}"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False
        except Exception:
            return False