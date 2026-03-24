import os
import sys
import subprocess

# Get the avni-ai subdirectory
script_dir = os.path.join(os.path.dirname(__file__), "avni-ai")

# Run the analytics script from the subdirectory
result = subprocess.run(
    [sys.executable, "run_analytics_test.py"],
    cwd=script_dir
)

sys.exit(result.returncode)
