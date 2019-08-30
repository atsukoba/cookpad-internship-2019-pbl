import json
from service import app

with open('config.json', 'r') as f:
    conf = json.load(f)

IP = conf['ip']
Port = conf['port']

if __name__ == "__main__":
    app.app.run(host=IP, port=Port, debug=True)
