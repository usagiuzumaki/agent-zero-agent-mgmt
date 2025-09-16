import asyncio
import select
import subprocess
import time
import sys
from typing import Optional, Tuple

class LocalInteractiveSession:
    def __init__(self):
        self.process = None
        self.full_output = ''

    async def connect(self):
        # Start a new subprocess with the appropriate shell for the OS
        if sys.platform.startswith('win'):
            # Windows
            self.process = subprocess.Popen(
                ['cmd.exe'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
        else:
            # macOS and Linux
            self.process = subprocess.Popen(
                ['/bin/bash'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

    def close(self):
        if self.process:
            self.process.terminate()
            self.process.wait()

    def send_command(self, command: str):
        if not self.process:
            raise Exception("Shell not connected")
        self.full_output = ""
        self.process.stdin.write(command + '\n') # type: ignore
        self.process.stdin.flush() # type: ignore
 
    async def read_output(self, timeout: float = 5.0, reset_full_output: bool = False) -> Tuple[str, Optional[str]]:
        if not self.process:
            raise Exception("Shell not connected")

        if timeout <= 0:
            raise ValueError("timeout must be positive")

        if reset_full_output:
            self.full_output = ""

        partial_output = ''
        start_time = time.time()

        while time.time() - start_time < timeout:
            stdout = self.process.stdout
            if stdout is None:
                break

            rlist, _, _ = select.select([stdout], [], [], 0.1)
            if not rlist:
                break  # No data available

            line = stdout.readline()  # type: ignore[arg-type]
            if not line:
                break  # No more output

            partial_output += line
            self.full_output += line

            # Give the subprocess a tiny bit of time to flush any
            # additional output before we loop back around.  This helps
            # avoid returning prematurely when commands emit output in
            # rapid bursts.
            await asyncio.sleep(0.1)

        if not partial_output:
            return self.full_output, None

        return self.full_output, partial_output
