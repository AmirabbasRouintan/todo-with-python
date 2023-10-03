import tkinter as tk
import pygame
from tkinter import messagebox, ttk
from datetime import datetime, time as dt_time
import pickle
from tkcalendar import Calendar
from time import strftime

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.configure(background="#282a36")

        self.tasks = []
        self.load_tasks()

        self.current_date_label = tk.Label(root, text="Current Date & Time:", background="#282a36", foreground="#ff79c6", font=('calibri', 20, 'bold'))
        self.current_date_label.pack()

        self.clock_label = tk.Label(root, font=('calibri', 12, 'bold'), background='purple', foreground='white')
        self.clock_label.pack(anchor='n', pady=10)

        self.update_clock()

        self.current_date = datetime.now().date()
        self.date_text = tk.StringVar()
        self.date_text.set(self.current_date.strftime("%Y-%m-%d"))
        self.date_label = tk.Label(root, textvariable=self.date_text, foreground="#50fa7b", background="#282a36", font=('calibri', 12, 'bold'))
        self.date_label.pack()

        self.calendar_label = tk.Label(root, text="Select Date:", background="#282a36", foreground="#ff79c6", font=('calibri', 15, 'bold'))
        self.calendar_label.pack()

        self.date_picker = Calendar(root, selectmode='day', date_pattern='yyyy-mm-dd')
        self.date_picker.pack()

        self.entry_frame = tk.Frame(root, background="#282a36")
        self.entry_frame.pack()

        self.task_label = tk.Label(self.entry_frame, text="Task:", background="#282a36", foreground="#f1fa8c", font=('calibri', 12, 'bold'))
        self.task_label.pack(side=tk.LEFT, padx=10, pady=5, anchor="e")

        self.task_entry = tk.Entry(self.entry_frame)
        self.task_entry.pack(side=tk.LEFT, padx=10, pady=5, anchor="w")

        self.hour_label = tk.Label(self.entry_frame, text="Hour:", background="#282a36", foreground="#f1fa8c", font=('calibri', 12, 'bold'))
        self.hour_label.pack(side=tk.LEFT, padx=10, pady=5, anchor="e")

        self.hour_entry = ttk.Combobox(self.entry_frame, values=[str(i).zfill(2) for i in range(1, 13)])
        self.hour_entry.pack(side=tk.LEFT, padx=10, pady=5, anchor="w")

        self.minute_label = tk.Label(self.entry_frame, text="Minute:", background="#282a36", foreground="#f1fa8c", font=('calibri', 12, 'bold'))
        self.minute_label.pack(side=tk.LEFT, padx=10, pady=5, anchor="e")

        self.minute_entry = ttk.Combobox(self.entry_frame, values=[str(i).zfill(2) for i in range(60)])
        self.minute_entry.pack(side=tk.LEFT, padx=10, pady=5, anchor="w")

        self.am_pm_label = tk.Label(self.entry_frame, text="AM/PM:", background="#282a36", foreground="#f1fa8c", font=('calibri', 12, 'bold'))
        self.am_pm_label.pack(side=tk.LEFT, padx=10, pady=5, anchor="e")

        self.am_pm_var = tk.StringVar()
        self.am_pm_var.set("AM")
        self.am_pm_entry = ttk.Combobox(self.entry_frame, values=["AM", "PM"], textvariable=self.am_pm_var)
        self.am_pm_entry.pack(side=tk.LEFT, padx=10, pady=5, anchor="w")

        self.task_listbox = tk.Listbox(root, font=("Helvetica", 14), height=10, width=70)
        self.task_listbox.pack()

        self.button_frame = tk.Frame(root, background="#282a36")
        self.button_frame.pack()

        self.add_button = tk.Button(self.button_frame, text="Add Task", command=self.add_task, bg="lightblue")
        self.add_button.pack(side=tk.LEFT, padx=10)

        self.start_button = tk.Button(self.button_frame, text="Start Timer", command=self.start_timer, bg="lightgreen")
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.edit_button = tk.Button(self.button_frame, text="Edit Task", command=self.edit_task, bg="orange")
        self.edit_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = tk.Button(self.button_frame, text="Delete Task", command=self.delete_task, bg="lightcoral")
        self.delete_button.pack(side=tk.LEFT, padx=10)

        self.clear_button = tk.Button(self.button_frame, text="Clear Tasks", command=self.clear_tasks, bg="lightyellow")
        self.clear_button.pack(side=tk.LEFT, padx=10)

        self.update_task_list()

        self.start_timer()

    def load_tasks(self):
        try:
            with open("tasks.pkl", "rb") as f:
                self.tasks = pickle.load(f)
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        with open("tasks.pkl", "wb") as f:
            pickle.dump(self.tasks, f)

    def update_clock(self):
        time_string = strftime('%H:%M:%S %p')
        self.clock_label.config(text=time_string)
        self.clock_label.after(1000, self.update_clock)

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task, time_obj, date_obj in self.tasks:
            self.task_listbox.insert(tk.END, f"{task} - {time_obj.strftime('%I:%M %p')} - {date_obj}")

    def add_task(self):
        task = self.task_entry.get()
        hour_str = self.hour_entry.get()
        minute_str = self.minute_entry.get()
        am_pm = self.am_pm_var.get()
        selected_date = self.date_picker.get_date()

        if task and hour_str and minute_str and am_pm and selected_date:
            try:
                hour = int(hour_str) if am_pm == "AM" else int(hour_str) + 12
                minute = int(minute_str)
                time_obj = dt_time(hour, minute)
                date_obj = selected_date
                self.tasks.append((task, time_obj, date_obj))
                self.save_tasks()
                self.update_task_list()
                self.task_entry.delete(0, tk.END)
                self.hour_entry.set('')
                self.minute_entry.set('')
                self.am_pm_var.set("AM")
                self.date_picker.set_date(self.current_date)
            except ValueError:
                messagebox.showerror("Error", "Invalid hour or minute.")
        else:
            messagebox.showerror("Error", "Please enter task, hour, minute, AM/PM, and date.")

    def clear_tasks(self):
        self.tasks = []
        self.save_tasks()
        self.update_task_list()

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            del self.tasks[index]
            self.save_tasks()
            self.update_task_list()

    def edit_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            if 0 <= index < len(self.tasks):
                updated_task = self.task_entry.get()
                updated_hour_str = self.hour_entry.get()
                updated_minute_str = self.minute_entry.get()
                updated_am_pm = self.am_pm_var.get()
                updated_date = self.date_picker.get_date()

                if updated_task and updated_hour_str and updated_minute_str and updated_am_pm and updated_date:
                    try:
                        updated_hour = int(updated_hour_str) if updated_am_pm == "AM" else int(updated_hour_str) + 12
                        updated_minute = int(updated_minute_str)
                        updated_time_obj = dt_time(updated_hour, updated_minute)
                        updated_date_obj = updated_date
                        self.tasks[index] = (updated_task, updated_time_obj, updated_date_obj)
                        self.save_tasks()
                        self.update_task_list()
                        self.task_entry.delete(0, tk.END)
                        self.hour_entry.set('')
                        self.minute_entry.set('')
                        self.am_pm_var.set("AM")
                        self.date_picker.set_date(self.current_date)
                    except ValueError:
                        messagebox.showerror("Error", "Invalid hour or minute.")
                else:
                    messagebox.showerror("Error", "Please enter task, hour, minute, AM/PM, and date.")
            else:
                messagebox.showerror("Error", "Please select a valid task to edit.")
        else:
            messagebox.showerror("Error", "Please select a task to edit.")

    def start_timer(self):
        def check_time():
            current_time = datetime.now().time()
            tasks_to_remove = []

            for task, time_obj, _ in self.tasks:
                if current_time >= time_obj:
                    if task not in tasks_to_remove:
                        tasks_to_remove.append(task)
                        pygame.mixer.init()
                        sound = pygame.mixer.Sound('alert.mp3')
                        sound.play()
                        messagebox.showinfo("Task Reminder", f"It's time to start '{task}'!")

            self.tasks = [(task, time_obj, date_obj) for task, time_obj, date_obj in self.tasks if task not in tasks_to_remove]
            self.root.after(60000, check_time)

        check_time()

def main():
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
