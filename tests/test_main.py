import subprocess
import sys


def test_main_output():
    result = subprocess.run([sys.executable, "-m", "src.main"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Hello from project_generator" in result.stdout
