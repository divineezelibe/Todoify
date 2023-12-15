from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

def add_task():
    task_string = task_field.get()
    if len(task_string) == 0:
        messagebox.showinfo('Error', 'Field is Empty.')
    else:
        tasks.append(task_string)
        the_cursor.execute('insert into tasks values (?)', (task_string,))
        list_update()
        task_field.delete(0, 'end')

def list_update():
    clear_list()
    for task in tasks:
        task_listbox.insert('end', task)

def delete_task():
    try:
        the_value = task_listbox.get(task_listbox.curselection())
        if the_value in tasks:
            tasks.remove(the_value)
            list_update()
            the_cursor.execute('delete from tasks where title = ?', (the_value,))
    except:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')

def delete_all_tasks():
    message_box = messagebox.askyesno('Delete All', 'Are you sure?')
    if message_box:
        while len(tasks) != 0:
            tasks.pop()
        the_cursor.execute('delete from tasks')
        list_update()

def clear_list():
    task_listbox.delete(0, 'end')

def close():
    print(tasks)
    guiWindow.destroy()

def retrieve_database():
    while len(tasks) != 0:
        tasks.pop()
    for row in the_cursor.execute('select title from tasks'):
        tasks.append(row[0])

if __name__ == "__main__":
    guiWindow = Tk()
    guiWindow.title("To-Do List ")
    guiWindow.geometry("665x400+550+250")
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg="#B5E5CF")

    the_connection = sql.connect('listOfTasks.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('create table if not exists tasks (title text)')

    tasks = []

    functions_frame = Frame(guiWindow, bg="white")
    functions_frame.pack(side="top", expand=True, fill="both", padx=10, pady=10)

    task_label = Label(
        functions_frame,
        text="Enter the Task:",
        font=("arial", 14, "bold"),
        background="black",
        foreground="white"
    )
    task_label.grid(row=0, column=0, pady=(10, 0), padx=10, sticky="w")

    task_field = Entry(
        functions_frame,
        font=("Arial", 14),
        width=42,
        foreground="black",
        background="white",
    )
    task_field.grid(row=0, column=1, pady=(10, 0), padx=10, sticky="w")

    button_style = {"width": 15, "font": ("arial", 14, "bold"), "bg": '#4CAF50', "fg": "white"}

    add_button = Button(
        functions_frame,
        text="Add Task",
        command=add_task,
        **button_style
    )
    del_button = Button(
        functions_frame,
        text="Delete Task",
        command=delete_task,
        **button_style
    )
    del_all_button = Button(
        functions_frame,
        text="Delete All Tasks",
        command=delete_all_tasks,
        **button_style
    )
    exit_button = Button(
        functions_frame,
        text="Exit",
        command=close,
        width=42,
        font=("arial", 14, "bold"),
        foreground='white',
        bg='#D41E0D',
    )

    add_button.grid(row=1, column=0, pady=(10, 0), padx=10, sticky="w")
    del_button.grid(row=1, column=1, pady=(10, 0), padx=10, sticky="w")
    del_all_button.grid(row=1, column=2, pady=(10, 0), padx=10, sticky="w")
    exit_button.grid(row=2, column=0, columnspan=4, pady=10, padx=10, sticky="w")

    task_listbox = Listbox(
        functions_frame,
        width=57,
        height=7,
        font=("Arial", 12),
        selectmode='SINGLE',
        background="WHITE",
        foreground="BLACK",
        selectbackground="#4CAF50",
        selectforeground="WHITE"
    )
    task_listbox.grid(row=3, column=0, columnspan=4, pady=10, padx=10, sticky="w")

    retrieve_database()
    list_update()

    guiWindow.mainloop()
    the_connection.commit()
    the_cursor.close()
