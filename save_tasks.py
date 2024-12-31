import json


tasks_file = "tasks.json"
def save_tasks(tasks):
    """
    Save tasks to a JSON file

    """
    with open(tasks_file, "w") as file:
        json.dump(tasks, file, indent=4)