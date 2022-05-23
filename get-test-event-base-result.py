import requests
from datetime import datetime
from sys import argv


key = argv[1]
event = argv[2]

req = requests.get("https://10.0.12.81/esmond/perfsonar/archive/{}/{}/base".format(key, event), verify=False)
data = req.json()

print("{} results found".format(len(data)))
if len(data) > 0: print("last record was at {}: {}".format(datetime.fromtimestamp(data[-1]['ts']).strftime("%d/%m/%Y %H:%M:%S"), data[-1]['val']))
