import threading
import time
import requests
import importlib, sys, os
from werkzeug.serving import make_server

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

app_mod = importlib.import_module('app')
flask_app = app_mod.app

HOST = '127.0.0.1'
PORT = 5000

server = make_server(HOST, PORT, flask_app)
thread = threading.Thread(target=server.serve_forever)
thread.daemon = True
thread.start()
print(f"Server started on http://{HOST}:{PORT}")

# Wait for server
time.sleep(1.0)

# Check /health
try:
    hr = requests.get(f'http://{HOST}:{PORT}/health', timeout=5)
    print('HEALTH:', hr.status_code, hr.json())
except Exception as e:
    print('HEALTH ERROR:', repr(e))

# Fetch /
try:
    r = requests.get(f'http://{HOST}:{PORT}/', timeout=5)
    print('HOME STATUS:', r.status_code)
    text = r.text
    print('HOME LENGTH:', len(text))
    print('HOME SNIPPET:', text[:200].replace('\n',' '))
except Exception as e:
    print('HOME ERROR:', repr(e))

# Shutdown
server.shutdown()
thread.join(timeout=5)
print('Server stopped')
