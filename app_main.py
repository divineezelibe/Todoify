from tkinter import *
from tkinter import ttk, messagebox
import sqlite3 as sql

class TodoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List")
        self.master.geometry("665x400+550+250")
        self.master.resizable(0, 0)
        self.master.configure(bg="#2E2E2E")

        self.tasks = []

        # Connect to the database
        self.connection = sql.connect('listOfTasks.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('create table if not exists tasks (title text)')

        # Frames
        sidebar_frame = Frame(master, bg="#1E1E1E")
        sidebar_frame.pack(side="left", fill="y", padx=(10, 5))

        main_frame = Frame(master, bg="#2E2E2E")
        main_frame.pack(side="left", fill="both", expand=True)

        # Labels
        task_label = Label(sidebar_frame, text="Enter the Task:", font=("Arial", 12), bg="#1E1E1E", fg="white")
        task_label.pack(pady=(30, 5), padx=10, anchor='w')

        # Entry Field
        self.task_field = Entry(sidebar_frame, font=("Arial", 12), width=20, bg="white", fg="black", bd=2, relief="groove", insertbackground="black")
        self.task_field.pack(padx=10)

        # Buttons
        button_style = {"style": "W.TButton", "padding": (10, 5), "width": 20, "command": None}

        add_button = ttk.Button(sidebar_frame, text="Add Task", **button_style)
        add_button.pack(pady=5)
        add_button.config(command=self.add_task)

        del_button = ttk.Button(sidebar_frame, text="Delete Task", **button_style)
        del_button.pack(pady=5)
        del_button.config(command=self.delete_task)

        del_all_button = ttk.Button(sidebar_frame, text="Delete All Tasks", **button_style)
        del_all_button.pack(pady=5)
        del_all_button.config(command=self.delete_all_tasks)

        exit_button = ttk.Button(sidebar_frame, text="Exit", **button_style)
        exit_button.pack(pady=5)
        exit_button.config(command=self.close)

        # Listbox
        self.task_listbox = Listbox(main_frame, width=57, height=20, font=("Arial", 12), selectmode='SINGLE', bg="#2E2E2E", fg="white", selectbackground="#D41E0D", selectforeground="white", bd=2, relief="groove")
        self.task_listbox.pack(pady=(20, 0), padx=10)

        # Call functions
        self.retrieve_database()
        self.list_update()

    def add_task(self):
        task_string = self.task_field.get()
        if len(task_string) == 0:
            messagebox.showinfo('Error', 'Field is Empty.')
        else:
            self.tasks.append(task_string)
            self.cursor.execute('insert into tasks values (?)', (task_string,))
            self.list_update()
            self.task_field.delete(0, 'end')

    def list_update(self):
        self.clear_list()
        for task in self.tasks:
            self.task_listbox.insert('end', task)

    def delete_task(self):
        try:
            the_value = self.task_listbox.get(self.task_listbox.curselection())
            if the_value in self.tasks:
                self.tasks.remove(the_value)
                self.list_update()
                self.cursor.execute('delete from tasks where title = ?', (the_value,))
        except:
            messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')

    def delete_all_tasks(self):
        message_box = messagebox.askyesno('Delete All', 'Are you sure?')
        if message_box:
            while len(self.tasks) != 0:
                self.tasks.pop()
            self.cursor.execute('delete from tasks')
            self.list_update()

    def clear_list(self):
        self.task_listbox.delete(0, 'end')

    def close(self):
        print(self.tasks)
        self.master.destroy()

    def retrieve_database(self):
        while len(self.tasks) != 0:
            self.tasks.pop()
        for row in self.cursor.execute('select title from tasks'):
            self.tasks.append(row[0])

if __name__ == '__main__':
    root = Tk()
    app = TodoApp(root)
    root.mainloop()
    app.connection.commit()
    app.cursor.close()
