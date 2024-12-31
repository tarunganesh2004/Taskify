import tkinter as tk
from tkinter import messagebox, ttk
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


def save_tasks(tasks):
    with open(tasks_file, "w") as file:
        json.dump(tasks, file, indent=4)

class TaskifyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Taskify - Task Manager")
        self.root.geometry("600x400")

        
        self.tasks = load_tasks()

        
        self.create_widgets()
        self.refresh_task_list()

    def create_widgets(self):
        # Title input
        tk.Label(self.root, text="Task Title:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.title_entry = tk.Entry(self.root, width=40)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        # Deadline 
        tk.Label(self.root, text="Deadline (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.deadline_entry = tk.Entry(self.root, width=40)
        self.deadline_entry.grid(row=1, column=1, padx=10, pady=5)

        # Add task button
        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Task list display
        self.tree = ttk.Treeview(self.root, columns=("Title", "Deadline"), show="headings")
        self.tree.heading("Title", text="Task Title")
        self.tree.heading("Deadline", text="Deadline")
        self.tree.column("Title", width=300)
        self.tree.column("Deadline", width=200)
        self.tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Delete task button
        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=4, column=0, columnspan=2, pady=10)

    def add_task(self):
        title = self.title_entry.get().strip()
        deadline = self.deadline_entry.get().strip()

        if not title or not deadline:
            messagebox.showerror("Error", "Both title and deadline are required.")
            return

        self.tasks.append({"title": title, "deadline": deadline})
        save_tasks(self.tasks)

        self.title_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)

        self.refresh_task_list()

    def delete_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a task to delete.")
            return

        for item in selected_item:
            task_index = self.tree.index(item)
            del self.tasks[task_index]

        save_tasks(self.tasks)
        self.refresh_task_list()

    def refresh_task_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for task in self.tasks:
            self.tree.insert("", "end", values=(task["title"], task["deadline"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskifyApp(root)
    root.mainloop()