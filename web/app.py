from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_bootstrap import Bootstrap
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = '6ry42r6pa867634puz'

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'divineezelibe.e@gmail.com'  # Replace with your Gmail address
app.config['MAIL_PASSWORD'] = 'gryr hcpz pabt cpuz'  # Replace with the generated App Password
app.config['MAIL_DEFAULT_SENDER'] = 'divineezelibe.e@gmail.com'
mail = Mail(app)
Bootstrap(app)

# Connect to the database
connection = sqlite3.connect('allTasks.db', check_same_thread=False)
cursor = connection.cursor()
cursor.execute('create table if not exists tasks (title text, datetime text, email text)')

def send_email(subject, body, recipient):
    msg = Message(subject, recipients=[recipient])
    msg.html = body
    mail.send(msg)

@app.route('/app', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task = request.form['task']
        due_date = request.form['due_date']
        email = request.form['email']

        if not task:
            flash('Task cannot be empty!', 'error')
        elif not email:
            flash('Email cannot be empty!', 'error')
        else:
            # Insert task into the database
            cursor.execute('insert into tasks (title, datetime, email) values (?, ?, ?)', (task, due_date, email))
            connection.commit()

            # Schedule email notification
            send_time = datetime.strptime(due_date, '%Y-%m-%dT%H:%M')
            delta = send_time - datetime.now()

            if delta.total_seconds() > 0:
                subject = 'Task Reminder'
                
                recipient = email

                send_time = datetime.now() + timedelta(seconds=delta.total_seconds())
                send_time_str = send_time.strftime('%Y-%m-%d %H:%M:%S')
                body = f"<h1>Todoify</h1><p><b>TASK</b> ({send_time_str}): {task}</p>"
                send_email(subject, body, recipient)
                flash('Task added and reminder scheduled!', 'success')
            else:
                flash('Invalid due date. Please choose a future date and time.', 'error')

    # Fetch tasks from the database
    cursor.execute('select title, datetime, email from tasks order by datetime')
    tasks = cursor.fetchall()

    return render_template('index.html', tasks=tasks)

@app.route('/', methods=['GET', 'POST'])
def landing():
    return render_template('landing.html')

@app.route('/delete/<task>')
def delete_task(task):
    # Delete task from the database
    cursor.execute('delete from tasks where title = ?', (task,))
    connection.commit()
    flash('Task deleted!', 'success')
    return redirect(url_for('index'))

@app.route('/delete_all')
def delete_all_tasks():
    # Delete all tasks from the database
    cursor.execute('delete from tasks')
    connection.commit()
    flash('All tasks deleted!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
