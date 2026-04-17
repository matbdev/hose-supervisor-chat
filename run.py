import subprocess
import sys

from dotenv import load_dotenv

# Load environment variables early to ensure they are available for imports
load_dotenv()

if __name__ == "__main__":
    # Launch Streamlit server targeting the app directory
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app/app.py"])
