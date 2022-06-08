import warnings
import requests
import json

from sys import argv


MACHINE_NAME = argv[1]
MACHINE_IP = argv[2] if len(argv) > 2 else MACHINE_NAME

BASE_URL = "https://10.0.12.81/pscheduler"

warnings.filterwarnings('ignore')

def get_task_schema (type: str, args: list):
  return requests.get(BASE_URL + f"/tests/{type}/spec", { "args": json.dumps(args) }, verify=False).json()

def get_tasks_info ():
  with open('config.json', 'r') as f:
    info = json.load(f)
    
  for i in range(len(info['tasks'])):
    info['tasks'][i]['args'].extend(['--dest', MACHINE_IP])

  return list(info.values())


def main ():
  tasks, schedule, archive = get_tasks_info()

  for task in tasks:
    task_definition = {
      "test": {
        "type": task['type'],
        "spec": get_task_schema(task['type'], task['args'])
      },
      "schedule": schedule,
      "archives": [ archive ]
    }

    print(f"Creating task for {task['type']} test...")
    print("Output: " + requests.post(BASE_URL + "/tasks", json=task_definition, verify=False).text)
    print()

if __name__ == '__main__':
  main()
