import requests
from datetime import datetime


req = requests.get("https://10.0.12.81/esmond/perfsonar/archive/", verify=False)

print(*["{} {:10s} ({} -> {}) updated at {:19s} with {} events".format(meta['metadata-key'], meta['pscheduler-test-type'], meta['source'], meta['destination'], datetime.fromtimestamp(max([e['time-updated'] for e in meta['event-types'] if e['time-updated'] is not None])).strftime("%d/%m/%Y %H:%M:%S"), len(meta['event-types'])) for meta in req.json()], sep='\n')
