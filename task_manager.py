import json
import os

tasks_file = "tasks.json"
def load_tasks():
    if os.path.exists(tasks_file):
        with open(tasks_file, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []  
    return []
