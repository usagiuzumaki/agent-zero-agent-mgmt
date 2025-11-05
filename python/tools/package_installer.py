"""
Package installation tool for Agent Zero
Works around sandboxing issues in deployed environments
"""
import subprocess
import sys
import json
from python.helpers.tool import Tool, Response

class PackageInstaller(Tool):
    """Install and manage Python packages"""
    
    async def execute(self, **kwargs):
        """Install packages directly without sandboxed execution"""
        action = kwargs.get("action", "install")
        packages = kwargs.get("packages", [])
        
        if not packages and action != "list":
            return Response(message="Please specify packages to install", break_loop=False)
        
        try:
            if action == "install":
                # Install packages using pip
                cmd = [sys.executable, "-m", "pip", "install"] + packages
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    message = f"✅ Successfully installed: {', '.join(packages)}\n{result.stdout}"
                else:
                    message = f"❌ Installation failed:\n{result.stderr}"
                    
            elif action == "uninstall":
                # Uninstall packages
                cmd = [sys.executable, "-m", "pip", "uninstall", "-y"] + packages
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    message = f"✅ Successfully uninstalled: {', '.join(packages)}"
                else:
                    message = f"❌ Uninstallation failed:\n{result.stderr}"
                    
            elif action == "list":
                # List installed packages
                cmd = [sys.executable, "-m", "pip", "list", "--format=json"]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    packages = json.loads(result.stdout)
                    package_list = [f"{p['name']}=={p['version']}" for p in packages[:20]]
                    message = f"📦 Installed packages (showing first 20):\n" + "\n".join(package_list)
                else:
                    message = f"❌ Failed to list packages:\n{result.stderr}"
                    
            else:
                message = f"❌ Unknown action: {action}. Use 'install', 'uninstall', or 'list'"
                
            return Response(message=message, break_loop=False)
            
        except subprocess.TimeoutExpired:
            return Response(message="⏰ Operation timed out", break_loop=False)
        except Exception as e:
            return Response(message=f"❌ Error: {str(e)}", break_loop=False)