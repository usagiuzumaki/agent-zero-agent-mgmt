"""
Enhanced code execution tool for deployed environments
Combines the best of both approaches to avoid sandboxing issues
"""
from python.helpers.tool import Tool, Response
from python.helpers.code_runner import DeploymentCodeRunner

class EnhancedCodeExecution(Tool):
    """Execute code reliably in deployed environments"""
    
    async def execute(self, **kwargs):
        """Run code with improved handling for deployed environments"""
        runtime = kwargs.get("runtime", "python").lower()
        code = kwargs.get("code", "")
        timeout = kwargs.get("timeout", 30)
        
        if not code:
            return Response(message="Please provide code to execute", break_loop=False)
        
        runner = DeploymentCodeRunner()
        
        try:
            if runtime == "python":
                success, output = await runner.run_python_code(code, timeout)
            elif runtime in ["terminal", "shell", "bash"]:
                success, output = await runner.run_shell_command(code, timeout)
            else:
                return Response(
                    message=f"Unsupported runtime: {runtime}. Use 'python' or 'terminal'",
                    break_loop=False
                )
            
            # Format the response
            if success:
                message = f"✅ Executed successfully:\n\n{output}"
            else:
                message = f"❌ Execution failed:\n\n{output}"
            
            # Truncate very long output
            if len(message) > 5000:
                message = message[:5000] + "\n\n[Output truncated...]"
            
            return Response(message=message, break_loop=False)
            
        except Exception as e:
            return Response(
                message=f"❌ Error during execution: {str(e)}",
                break_loop=False
            )