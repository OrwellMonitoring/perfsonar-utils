from time import sleep, time
from datetime import datetime
from kafka import KafkaProducer
import requests
import warnings
import logging
import json
import math


warnings.filterwarnings('ignore')
BASE_URL = "https://10.0.13.69"
SLEEP_TIME_SECONDS = 60*10

optional_props = {
  'ip-transport-protocol': 'protocol'
}

while True:
  KAFKA_URL= requests.get("http://10.0.12.82:8008/service_discovery/kafka/").text

  req = requests.get(BASE_URL + "/esmond/perfsonar/archive/", verify=False)
  data = req.json()

  data = [
    {
      'test-type': test['pscheduler-test-type'],
      'source': test['source'],
      'destination': test['destination'],
      'measurement-agent': test['measurement-agent'],
      **{ prop: test[prop] for prop, _ in optional_props.items() if prop in test.keys() },
      'event-types': [
        {
          'url': event['base-uri'],
          'event': event['event-type'],
          'summaries': [
            {
              'url': summary['uri'],
              'event': event['event-type'] + '_' + summary['summary-type'] + '_' + summary['summary-window'],
            }
            for summary in event['summaries']
          ]
        }
        for event in test['event-types']
      ]
    }
    for test in data
  ]

  metrics = [
    {
      'metric': 'network_' + event['event'].replace('-', '_'),
      'props': {
        'test_type': test['test-type'],
        'source': test['source'],
        'destination': test['destination'],
        'measurement_agent': test['measurement-agent'],
        **{ name: test[prop] for prop, name in optional_props.items() if prop in test.keys() }
      },
      'value': metric['val'],
      'ts': metric['ts']
    }
    for test in data
    for event in test['event-types']
    for metric in requests.get(BASE_URL + event['url'], verify=False).json()[-1:-2:-1]
  ] \
  + \
  [
    {
      'metric': 'network_' + summary['event'].replace('-', '_'),
      'props': {
        'test_type': test['test-type'],
        'source': test['source'],
        'destination': test['destination'],
        'measurement_agent': test['measurement-agent'],
        **{ name: test[prop] for prop, name in optional_props.items() if prop in test.keys() }
      },
      'value': metric['val'],
      'ts': metric['ts']
    }
    for test in data
    for event in test['event-types']
    for summary in event['summaries']
    for metric in requests.get(BASE_URL + summary['url'], verify=False).json()[-1:-2:-1]
  ]

  PAGE_SIZE = 20
  for i in range(math.ceil(len(metrics)/PAGE_SIZE)):
    packet = metrics[i*PAGE_SIZE:(i+1)*PAGE_SIZE]
    for metric in packet: print(metric['metric'])
    KafkaProducer(bootstrap_servers=[KAFKA_URL]).send('perf', json.dumps(packet).encode('ascii'))

  print("Next run at " + datetime.fromtimestamp(time() + SLEEP_TIME_SECONDS).strftime('%d-%m-%Y %I:%M:%S'))
  sleep(SLEEP_TIME_SECONDS)
