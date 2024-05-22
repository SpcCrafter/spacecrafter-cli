import json
import os
from datetime import datetime, timedelta

TOKEN_FILE = os.path.expanduser('~/.spc_token')
TOKEN_EXPIRY_HOURS = 12

def save_token(token):
    with open(TOKEN_FILE, 'w') as f:
        expiry_time = datetime.now() + timedelta(hours=TOKEN_EXPIRY_HOURS)
        f.write(json.dumps({'token': token, 'expiry': expiry_time.isoformat()}))

def load_token():
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, 'r') as f:
        data = json.load(f)
        expiry_time = datetime.fromisoformat(data['expiry'])
        if datetime.now() < expiry_time:
            return data['token']
    return None
