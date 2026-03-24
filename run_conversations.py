import os
import sys
import subprocess

# Get the avni-ai subdirectory
script_dir = os.path.join(os.path.dirname(__file__), "avni-ai")

# Run the conversations analysis script from the subdirectory
result = subprocess.run(
    [sys.executable, "run_conversations_analysis.py"],
    cwd=script_dir
)

sys.exit(result.returncode)
