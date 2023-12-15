from tkinter import *
from tkinter import messagebox
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
        sidebar_frame.pack(side="left", fill="y")

        main_frame = Frame(master, bg="#2E2E2E")
        main_frame.pack(side="left", fill="both", expand=True)

        # Labels
        task_label = Label(sidebar_frame, text="Enter the Task:", font=("Arial", 14), bg="#1E1E1E", fg="white")
        task_label.pack(pady=(30, 10))

        # Entry Field
        self.task_field = Entry(sidebar_frame, font=("Arial", 14), width=20, bg="white", fg="black")
        self.task_field.pack()

        # Buttons
        add_button = Button(sidebar_frame, text="Add Task", width=15, font=("Arial", 14, "bold"), bg='#D41E0D', fg="white", command=self.add_task)
        add_button.pack(pady=10)
        
        del_button = Button(sidebar_frame, text="Delete Task", width=15, font=("Arial", 14, "bold"), bg='#D41E0D', fg="white", command=self.delete_task)
        del_button.pack(pady=10)

        del_all_button = Button(sidebar_frame, text="Delete All Tasks", width=15, font=("Arial", 14, "bold"), bg='#D41E0D', fg="white", command=self.delete_all_tasks)
        del_all_button.pack(pady=10)

        exit_button = Button(sidebar_frame, text="Exit", width=15, font=("Arial", 14, "bold"), bg='#D41E0D', fg="white", command=self.close)
        exit_button.pack(pady=10)

        # Listbox
        self.task_listbox = Listbox(main_frame, width=57, height=20, font="bold", selectmode='SINGLE', bg="#2E2E2E", fg="white", selectbackground="#D41E0D", selectforeground="white")
        self.task_listbox.pack(pady=(20, 0))

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
