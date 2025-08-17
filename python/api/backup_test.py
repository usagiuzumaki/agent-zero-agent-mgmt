"""API endpoint to test backup file selection patterns.

Pytest attempts to collect any file ending with ``_test.py`` as a test
module.  When run from the repository root the absolute imports used here
(`python.helpers...`) fail because the ``python`` package isn't installed on
the import path.  Using package-relative imports avoids this issue and keeps
the module importable both by the application and by the test runner without
requiring any path manipulation.
"""

from ..helpers.api import ApiHandler, Request, Response
from ..helpers.backup import BackupService


class BackupTest(ApiHandler):
    @classmethod
    def requires_auth(cls) -> bool:
        return True

    @classmethod
    def requires_loopback(cls) -> bool:
        return False

    async def process(self, input: dict, request: Request) -> dict | Response:
        try:
            # Get input parameters
            include_patterns = input.get("include_patterns", [])
            exclude_patterns = input.get("exclude_patterns", [])
            include_hidden = input.get("include_hidden", False)
            max_files = input.get("max_files", 1000)

            # Support legacy string patterns format for backward compatibility
            patterns_string = input.get("patterns", "")
            # Only parse legacy patterns string when pattern arrays are absent
            # to maintain backward compatibility without mixing formats.
            if patterns_string and not include_patterns and not exclude_patterns:
                # Parse patterns string into arrays
                lines = [line.strip() for line in patterns_string.split('\n') if line.strip() and not line.strip().startswith('#')]
                for line in lines:
                    if line.startswith('!'):
                        exclude_patterns.append(line[1:])
                    else:
                        include_patterns.append(line)

            if not include_patterns:
                return {
                    "success": True,
                    "files": [],
                    "total_count": 0,
                    "truncated": False
                }

            # Create metadata object for testing
            metadata = {
                "include_patterns": include_patterns,
                "exclude_patterns": exclude_patterns,
                "include_hidden": include_hidden
            }

            backup_service = BackupService()
            matched_files = await backup_service.test_patterns(metadata, max_files=max_files)

            return {
                "success": True,
                "files": matched_files,
                "total_count": len(matched_files),
                "truncated": len(matched_files) >= max_files
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
