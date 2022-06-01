from orwell import Metric, Runner
import json


def translate (line: str) -> list:
  data = json.loads(line)
  metrics = []

  for metric in data:
    if type(metric['value']) == list: metric['value'] = metric['value'][-1] if len(metric['value']) > 0 else None
    if metric['value'] is None: continue
    
    if type(metric['value']) == dict:
      if len(metric['value'].items()) <= 500:
        for name, val in metric['value'].items():
          
          if type(val) in [int, float]: metrics.append(Metric(metric['metric'], str(val), { 'key': name, **metric['props'] }, metric['ts'], 'perf'))
          else: print(type(val))

      else: print("Big value " + metric['metric'])
    else:
        metrics.append(Metric(metric['metric'], str(metric['value']), metric['props'], metric['ts'], 'perf'))
        
  return metrics

translator = Runner(translate)
translator.run()