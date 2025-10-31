import requests
import sys

HOST = 'http://127.0.0.1:5000'

def send(msg):
    try:
        r = requests.post(HOST + '/chat', json={'message': msg}, timeout=5)
        print('->', msg)
        print(r.status_code, r.json())
    except Exception as e:
        print('Error sending', msg, e)

if __name__ == '__main__':
    messages = ['hi', 'where is my order', 'what is your return policy', 'thank you']
    for m in messages:
        send(m)
