import threading
import time
import requests
import importlib, sys, os
from werkzeug.serving import make_server

# Ensure project root is importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

app_mod = importlib.import_module('app')
flask_app = app_mod.app

HOST = '127.0.0.1'
PORT = 5001

server = make_server(HOST, PORT, flask_app)
thread = threading.Thread(target=server.serve_forever)
thread.daemon = True
thread.start()
print(f"Server started on http://{HOST}:{PORT}")

# Wait briefly for server readiness
time.sleep(1.0)

messages = ['hi', 'where is my order', 'order #12345', 'what is your return policy', 'thanks']

for m in messages:
    try:
        r = requests.post(f'http://{HOST}:{PORT}/chat', json={'message': m}, timeout=5)
        try:
            body = r.json()
        except Exception:
            body = r.text
        print('---')
        print('MSG:', m)
        print('STATUS:', r.status_code)
        print('BODY:', body)
    except Exception as e:
        print('---')
        print('MSG:', m)
        print('ERROR:', repr(e))

# Shutdown
print('Shutting down server...')
server.shutdown()
thread.join(timeout=5)
print('Server stopped')
