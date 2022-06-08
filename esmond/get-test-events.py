import requests
from datetime import datetime
from sys import argv


key = argv[1]

req = requests.get("https://10.0.12.81/esmond/perfsonar/archive/" + key, verify=False)
data = req.json()

print("{:10s} ({} -> {})".format(data['pscheduler-test-type'], data['source'], data['destination']))
print(*["{:35s} (last updated: {:20s}; summaries: {} - [{}])".format(meta['event-type'], datetime.fromtimestamp(meta['time-updated']).strftime("%d/%m/%Y %H:%M:%S") if meta['time-updated'] else 'Never', len(meta['summaries']), ', '.join(["{} {}s".format(s['summary-type'], s['summary-window']) for s in meta['summaries']])) for meta in req.json()['event-types']], sep='\n')
