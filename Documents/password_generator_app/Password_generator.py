import sqlite3

# Connect to the database
db_connection = sqlite3.connect('password_manager.db')
cursor = db_connection.cursor()

# Create a table containing the passwords from data breaches
cursor.execute('''
    CREATE TABLE IF NOT EXISTS leaked_passwords (
        id INTEGER PRIMARY KEY,
        website TEXT,
        Username TEXT,
        password TEXT
    )
''')
# Create a table containing users new passwords
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users_passwords (
        id INTEGER PRIMARY KEY,
        website TEXT,
        Username TEXT,
        password TEXT
    )
''')
# Simulate data from a data breach
data_breach = [
    ('Facebook.com','user1','password123'),
    ('Google.com','user2','securepassword'),
    ('HSBC.com','user3','bankpass123'),
    ('Twitter.com','user4','socialpass'),
]
# Insert data into the table
cursor.executemany(
    'INSERT INTO leaked_passwords (website, Username, password) VALUES (?, ?, ?)', data_breach)

# Commit changes and close the connection
db_connection.commit()
db_connection.close()























import sqlite3
import database.py
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import sqlite3




# Connect to the database
db_connection = sqlite3.connect('password_manager.db')
cursor = db_connection.cursor()
# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS leaked_passwords (
        id INTEGER PRIMARY KEY,
        website TEXT,
        Username TEXT,
        password TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users_passwords (
        id INTEGER PRIMARY KEY,
        website TEXT,
        Username TEXT,
        password TEXT
    )
''')
# Simulate data from a data breach
data_breach = [
    ('Facebook.com', 'user1', 'password123'),
    ('Google.com', 'user2', 'securepassword'),
    ('HSBC.com', 'user3', 'bankpass123'),
    ('Twitter.com', 'user4', 'socialpass'),
]
# Insert data into the table
cursor.executemany(
    'INSERT INTO leaked_passwords (website, Username, password) VALUES (?, ?, ?)', data_breach)

# Commit changes and close the connection
db_connection.commit()


# Fetch all leaked passwords
cursor.execute('SELECT * FROM leaked_passwords')
records = cursor.fetchall()
leak_from_db = [record[3] for record in records]
# Fetch all user passwords
cursor.execute('SELECT * FROM users_passwords')
records = cursor.fetchall()
user_from_db = [record[3] for record in records]
db_connection.close()
# Function to insert into leaked db
def insert_into_leakeddb(data):
    if len(data) == 3:  # Check if the data has the correct number of elements
        with sqlite3.connect('password_manager.db') as db_connection:
            cursor = db_connection.cursor()
            cursor.execute('''INSERT INTO 
                        leaked_passwords(website, Username, password) 
                        VALUES (?, ?, ?)''',
                       data)
            db_connection.commit()
# Function to insert into user db
def insert_into_userdb(data):
    if len(data) == 3:
        with sqlite3.connect('password_manager.db') as db_connection:
            cursor = db_connection.cursor()
            cursor.execute('''INSERT INTO 
                        users_passwords(website, Username, password) 
                        VALUES (?, ?, ?)''',
                       data)
            db_connection.commit()


def generate_password():
    letters = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)]
    numbers = [str(i) for i in range(10)]
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = random.choices(letters, k=random.randint(7, 10)) + \
                    random.choices(symbols, k=random.randint(3, 5)) + \
                    random.choices(numbers, k=random.randint(3, 5))

    random.shuffle(password_list)
    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
def save_user_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if password in leak_from_db:
        messagebox.showinfo(title="Leaked Password",
                            message="This password is in the leaked passwords database. Please choose a different one.")
        return

    if password in user_from_db:
        result = messagebox.askokcancel(title="Used Password",
                                        message="You have already used this password. Do you want to proceed?")
        if not result:
            return
    insert_into_userdb((website, email, password))
    website_entry.delete(0, END)
    password_entry.delete(0, END)

def update_password():
    website = website_entry.get()
    email = email_entry.get()  # Using email as a form of user identification
    new_password = password_entry.get()
    
    if not website or not email or not new_password:
        messagebox.showinfo(title="Empty Fields", message="Please make sure all fields are filled.")
        return

    with sqlite3.connect('password_manager.db') as db_connection:
        cursor = db_connection.cursor()

        cursor.execute('SELECT password FROM users_passwords WHERE website = ? AND Username = ?', (website, email))
        record = cursor.fetchone()

        if record:
            result = messagebox.askokcancel(title="Update Password",
                                            message=f"Existing password for {website} found. Do you want to update it?")
            if result:
                cursor.execute('UPDATE users_passwords SET password = ? WHERE website = ? AND Username = ?', 
                               (new_password, website, email))
                db_connection.commit()
                messagebox.showinfo(title="Password Updated", message=f"Password for {website} has been updated!")
        else:
            messagebox.showinfo(title="No Record Found", message=f"No existing password for {website} found. Please add it first.")

    website_entry.delete(0, END)
    email_entry.delete(0, END)
    password_entry.delete(0, END)


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")

canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)
# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)
# Entries
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "angela@gmail.com")
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)
# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=36, command=save_user_password)
add_button.grid(row=4, column=1, columnspan=2)
update_button = Button(text="Update Password", width=36, command=update_password)
update_button.grid(row=5, column=1, columnspan=2)
window.mainloop()
