import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttks
from plyer import notification
import subprocess
import bcrypt 
import os 

def create_admin_login_window():
    global window
    window = ttks.Style(theme='morph').master
    window.title("Admin Login")
    window.geometry('600x300')

    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 20))
    style.configure('TButtonHover', font=('Helvetica', 20), background='#ADD8E6') 

    frame = ttk.Frame(window)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    ttk.Label(frame, text="Please enter your credentials:", font=('Helvetica', 24)).grid(column=0, row=0, padx=10, pady=10)

    ttk.Label(frame, text="Username:", font=('Helvetica', 20)).grid(column=0, row=1, padx=10, pady=10)
    username_entry = ttk.Entry(frame)
    username_entry.grid(column=1, row=1)

    ttk.Label(frame, text="Password:", font=('Helvetica', 20)).grid(column=0, row=2, padx=10, pady=10)
    password_entry = ttk.Entry(frame)
    password_entry.grid(column=1, row=2)

    login_button = ttk.Button(frame, text="Login", command=lambda: admin_login(username_entry.get(), password_entry.get()), style='TButton')
    login_button.grid(column=1, row=3, pady=20)

    window.mainloop()


def admin_login(username, password):
    passw = 'process2023-2' 
    salt = bcrypt.gensalt() 
    stored_password = bcrypt.hashpw(passw.encode(), salt) 
    if username == 'admin' and bcrypt.checkpw(password.encode(), stored_password): 
        notification.notify(
            title="Login Successful",
            message="You have successfully logged in as admin.",
            timeout=10
        )
        window.destroy()
        subprocess.run(['python', 'C:\\Users\\PC01A\\Downloads\\MiniProyecto\\AdminModule\\adminModule.py'])

    else:
        notification.notify(
            title="Wrong Password or Username",
            message="Try again!",
            timeout=10
        )

create_admin_login_window()
