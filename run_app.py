# run_app.py
import subprocess
import sys
import time
import webbrowser
import socket
import os

APP_FILE = os.environ.get("IOM_APP_FILE", "main.py")   # muokkaa tarvittaessa
HOST = os.environ.get("IOM_HOST", "0.0.0.0")          # 0.0.0.0 -> kuuntelee kaikissa verkoissa
PORT = int(os.environ.get("IOM_PORT", "8501"))        # vaihda tarvittaessa

def is_port_open(host, port):
    """Tarkistaa kuunteleeko jokin prosessi annetulla portilla paikalliskoneella."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.2)
        return s.connect_ex(("127.0.0.1" if host == "0.0.0.0" else host, port)) == 0

def main():
    # Streamlit-käynnistys sisäverkkoa varten:
    # - --server.address 0.0.0.0: kuuntelee kaikissa interfacessä (LAN/WLAN)
    # - --server.port <PORT>: määritetty portti
    # - --server.headless false: avaa selaimen paikallisesti
    # Huom: CORS/XSRF oletuksilla turvataan käyttöä; sisäverkossa voi tarvittaessa säätää.
    cmd = [
        sys.executable, "-m", "streamlit", "run", APP_FILE,
        "--server.port", str(PORT),
        "--server.address", HOST,
        "--server.headless", "false",
        # Valinnainen: jos tarvitset helpomman sisäverkkotestin ilman CORS/XSRF:
        # "--server.enableCORS", "false",
        # "--server.enableXsrfProtection", "false",
    ]

    # Käynnistä Streamlit-prosessi
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # Odota, että palvelin nousee, ja avaa selain paikallisesti
    for _ in range(120):  # max ~60s odotus (120 * 0.5s)
        if is_port_open(HOST, PORT):
            # Avaa paikallisesti selain (käyttäjäkoneella)
            webbrowser.open(f"http://localhost:{PORT}")
            break
        time.sleep(0.5)

    # Pidä wrapper hengissä Streamlitin ajan
    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()

if __name__ == "__main__":
    main()
