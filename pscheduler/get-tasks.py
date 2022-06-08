import requests


tasks = requests.get("https://10.0.12.81/pscheduler/tasks", verify=False).json()
tasks = [ requests.get(url, verify=False).json() for url in tasks ]
