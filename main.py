import tkinter as tk
from notification_manager import TaskifyProApp

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskifyProApp(root)
    root.mainloop()