import os
import sys
import subprocess

script_dir = os.path.join(os.path.dirname(__file__), "avni-ai")
result = subprocess.run([sys.executable, "run_analytics_test.py"], cwd=script_dir)
sys.exit(result.returncode)
