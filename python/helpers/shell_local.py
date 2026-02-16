import asyncio
import sys
import time
from typing import Optional, Tuple

class LocalInteractiveSession:
    def __init__(self):
        self.process: Optional[asyncio.subprocess.Process] = None
        self.full_output = ''

    async def connect(self):
        # Start a new subprocess with the appropriate shell for the OS
        if sys.platform.startswith('win'):
            # Windows
            self.process = await asyncio.create_subprocess_exec(
                'cmd.exe',
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                creationflags=0x08000000 # CREATE_NO_WINDOW
            )
        else:
            # macOS and Linux
            self.process = await asyncio.create_subprocess_exec(
                '/bin/bash',
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

    async def close(self):
        if self.process:
            try:
                self.process.terminate()
                await self.process.wait()
            except:
                pass

    async def send_command(self, command: str):
        if not self.process or not self.process.stdin:
            raise Exception("Shell not connected")
        self.full_output = ""
        self.process.stdin.write((command + '\n').encode())
        await self.process.stdin.drain()
 
    async def read_output(self, timeout: float = 5.0, reset_full_output: bool = False) -> Tuple[str, Optional[str]]:
        if not self.process or not self.process.stdout:
            raise Exception("Shell not connected")

        if timeout <= 0:
            raise ValueError("timeout must be positive")

        if reset_full_output:
            self.full_output = ""

        partial_output = ''
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                # Use wait_for to implement a timeout on the read operation
                # We read one line at a time
                line_bytes = await asyncio.wait_for(self.process.stdout.readline(), timeout=0.1)
                if not line_bytes:
                    break  # End of stream

                line = line_bytes.decode(errors='replace')
                partial_output += line
                self.full_output += line

                # Give the subprocess a tiny bit of time to flush any
                # additional output before we loop back around.
                await asyncio.sleep(0.1)
            except asyncio.TimeoutError:
                # No data available within the short timeout
                break
            except Exception as e:
                # Possible issues like decoding or stream errors
                break

        if not partial_output:
            return self.full_output, None

        return self.full_output, partial_output
