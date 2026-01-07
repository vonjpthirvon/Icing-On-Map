import subprocess
import sys

def main():
    # Käynnistää Streamlit-sovelluksen
    subprocess.run([sys.executable, "-m", "streamlit", "run", "main.py"])

if __name__ == "__main__":
    main()
