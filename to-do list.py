import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import os

class ToDoList:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List Application")
        self.master.geometry("400x400")

        self.tasks = self.load_tasks()

        self.task_listbox = tk.Listbox(self.master, selectmode=tk.SINGLE, height=15, width=40)
        self.task_listbox.pack(pady=10)

        self.refresh_tasks()

        self.add_button = tk.Button(self.master, text="Add Task", command=self.show_add_task_window)
        self.add_button.pack(pady=5)

        self.remove_button = tk.Button(self.master, text="Remove Task", command=self.remove_task)
        self.remove_button.pack(pady=5)

        self.mark_completed_button = tk.Button(self.master, text="Mark as Completed", command=self.mark_as_completed)
        self.mark_completed_button.pack(pady=5)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def refresh_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = " (Completed)" if task.get('completed', False) else ""
            priority = f" - Priority: {task['priority']}"
            due_date = f" - Due Date: {task['due_date']}" if task.get('due_date') else ""
            self.task_listbox.insert(tk.END, f"{task['title']}{priority}{due_date}{status}")

    def load_tasks(self):
        file_path = 'tasks.json'
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
        else:
            return []

    def save_tasks(self):
        with open('tasks.json', 'w') as file:
            json.dump(self.tasks, file, indent=2)

    def show_add_task_window(self):
        add_task_window = tk.Toplevel(self.master)
        add_task_window.title("Add Task")

        tk.Label(add_task_window, text="Task Title:").pack()
        title_entry = tk.Entry(add_task_window)
        title_entry.pack()

        tk.Label(add_task_window, text="Priority:").pack()
        priority_entry = tk.Entry(add_task_window)
        priority_entry.pack()

        tk.Label(add_task_window, text="Due Date (YYYY-MM-DD):").pack()
        due_date_entry = tk.Entry(add_task_window)
        due_date_entry.pack()

        add_button = tk.Button(add_task_window, text="Add Task", command=lambda: self.add_task(
            title_entry.get(), priority_entry.get(), due_date_entry.get(), add_task_window
        ))
        add_button.pack(pady=10)

    def add_task(self, title, priority, due_date, add_task_window):
        new_task = {'title': title, 'priority': priority, 'due_date': due_date}
        self.tasks.append(new_task)
        self.save_tasks()
        self.refresh_tasks()
        add_task_window.destroy()

    def remove_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            confirmed = messagebox.askyesno("Confirm", "Are you sure you want to remove this task?")
            if confirmed:
                del self.tasks[selected_index[0]]
                self.save_tasks()
                self.refresh_tasks()
        else:
            messagebox.showwarning("Warning", "Please select a task to remove.")

    def mark_as_completed(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task = self.tasks[selected_index[0]]
            task['completed'] = True
            self.save_tasks()
            self.refresh_tasks()
        else:
            messagebox.showwarning("Warning", "Please select a task to mark as completed.")

    def on_closing(self):
        confirmed = messagebox.askyesno("Confirm", "Do you want to exit the application?")
        if confirmed:
            self.master.destroy()

def main():
    root = tk.Tk()
    app = ToDoList(root)
    root.mainloop()

if __name__ == "__main__":
    main()
