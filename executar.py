import os
import subprocess
import sys

pasta = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], cwd=pasta)
