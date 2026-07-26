import subprocess
import sys
import unittest
from pathlib import Path


class DeploymentConfigurationTests(unittest.TestCase):
    def test_production_settings_load(self):
        repo_root = Path(__file__).resolve().parent
        result = subprocess.run(
            [sys.executable, "manage.py", "check", "--settings=config.settings.production"],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )

        self.assertEqual(
            result.returncode,
            0,
            msg=f"Production startup check failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}",
        )


if __name__ == "__main__":
    unittest.main()
