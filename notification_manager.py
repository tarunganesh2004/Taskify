from datetime import datetime,timedelta
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar
from save_tasks import save_tasks
from task_manager import load_tasks

class TaskifyProApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Taskify Pro - Advanced Task Manager")
        self.root.geometry("800x600")

        # Task list storage
        self.tasks = load_tasks()

        # UI Elements
        self.create_widgets()
        self.refresh_task_list()
        self.setup_notification_checker()

    def create_widgets(self):
        # Styling
        self.root.style = ttk.Style()
        self.root.style.theme_use("clam")

        # Title input
        tk.Label(self.root, text="Task Title:").grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        self.title_entry = tk.Entry(self.root, width=30)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        # Deadline input
        tk.Label(self.root, text="Deadline (YYYY-MM-DD):").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        self.deadline_entry = tk.Entry(self.root, width=30)
        self.deadline_entry.grid(row=1, column=1, padx=10, pady=5)

        # Priority input
        tk.Label(self.root, text="Priority:").grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )
        self.priority_combo = ttk.Combobox(
            self.root, values=["High", "Medium", "Low"], state="readonly", width=27
        )
        self.priority_combo.grid(row=2, column=1, padx=10, pady=5)
        self.priority_combo.set("Medium")

        # Add task button
        self.add_button = tk.Button(
            self.root, text="Add Task", command=self.add_task, bg="green", fg="white"
        )
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Task list display
        self.tree = ttk.Treeview(
            self.root, columns=("Title", "Deadline", "Priority"), show="headings"
        )
        self.tree.heading("Title", text="Task Title")
        self.tree.heading("Deadline", text="Deadline")
        self.tree.heading("Priority", text="Priority")
        self.tree.column("Title", width=250)
        self.tree.column("Deadline", width=150)
        self.tree.column("Priority", width=100)
        self.tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Delete task button
        self.delete_button = tk.Button(
            self.root,
            text="Delete Task",
            command=self.delete_task,
            bg="red",
            fg="white",
        )
        self.delete_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Calendar widget
        tk.Label(self.root, text="Calendar View:").grid(
            row=0, column=2, padx=10, pady=5, sticky="w"
        )
        self.calendar = Calendar(self.root, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendar.grid(row=1, column=2, rowspan=4, padx=10, pady=5)

    def add_task(self):
        title = self.title_entry.get().strip()
        deadline = self.deadline_entry.get().strip()
        priority = self.priority_combo.get().strip()

        if not title or not deadline or not priority:
            messagebox.showerror(
                "Error", "All fields (title, deadline, priority) are required."
            )
            return

        try:
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
            return

        self.tasks.append({"title": title, "deadline": deadline, "priority": priority})
        save_tasks(self.tasks)

        self.title_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)
        self.priority_combo.set("Medium")

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
            self.tree.insert(
                "", "end", values=(task["title"], task["deadline"], task["priority"])
            )

    def setup_notification_checker(self):
        self.check_notifications()

    def check_notifications(self):
        now = datetime.now()
        for task in self.tasks:
            task_deadline = datetime.strptime(task["deadline"], "%Y-%m-%d")
            if now <= task_deadline <= now + timedelta(days=1):
                messagebox.showinfo(
                    "Upcoming Deadline",
                    f"Task '{task['title']}' is due soon (Deadline: {task['deadline']}).",
                )
        self.root.after(60000, self.check_notifications)  # Check every minute
