import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttks
import subprocess

def create_login_window():
    global window
    window = ttks.Style(theme='morph').master
    window.title("Login")
    window.geometry('500x300')

    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 20))
    style.configure('TButtonHover', font=('Helvetica', 20), background='#ADD8E6')

    frame = ttk.Frame(window)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    ttk.Label(frame, text="Please select your role:", font=('Helvetica', 24)).grid(column=0, row=0, padx=10, pady=10)

    admin_button = ttk.Button(frame, text="Admin", command=admin_login, style='TButton')
    admin_button.grid(column=0, row=1, pady=20)

    vendor_button = ttk.Button(frame, text="Vendor", command=vendor_login, style='TButton')
    vendor_button.grid(column=0, row=2)

    window.mainloop()


def admin_login():
    window.destroy()
    subprocess.run(['python', 'C:\\Users\\PC01A\\Downloads\\MiniProyecto\\AdminModule\\adminLoginModule.py'])

def vendor_login():
    window.destroy()
    subprocess.run(['python', 'C:\\Users\\PC01A\\Downloads\\MiniProyecto\\VendorModule\\vendorLoginModule.py'])


create_login_window()
