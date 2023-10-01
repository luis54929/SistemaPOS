import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttks
import sqlite3
import os # Importamos el módulo os para usar rutas relativas
import tkinter.messagebox 

def create_vendor_login_window():
    global window
    window = ttks.Style(theme='morph').master
    window.title("Vendor Login")
    window.geometry('800x300')

    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 20))
    style.configure('TButtonHover', font=('Helvetica', 20), background='#ADD8E6')

    frame = ttk.Frame(window)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    ttk.Label(frame, text="Please enter your credentials:", font=('Helvetica', 24)).grid(column=0, row=0, padx=10, pady=10)

    ttk.Label(frame, text="ID:", font=('Helvetica', 20)).grid(column=0, row=1, padx=10, pady=10)
    user_entry = ttk.Entry(frame)
    user_entry.grid(column=1, row=1)

    ttk.Label(frame, text="Password:", font=('Helvetica', 20)).grid(column=0, row=2, padx=10, pady=10)
    password_entry = ttk.Entry(frame)
    password_entry.grid(column=1, row=2)

    login_button = ttk.Button(frame, text="Login", command=lambda: vendor_login(user_entry.get(), password_entry.get()), style='TButton')
    login_button.grid(column=1, row=3, pady=20)

    window.mainloop()


def vendor_login(id_, password):
    # Conectar a la base de datos
    conn = sqlite3.connect('C:\\Users\\PC01A\\Downloads\\MiniProyecto\\DBMP\\vendors.sqlite')
    cursor = conn.cursor()

    # Validar los datos del usuario
    cursor.execute("SELECT * FROM vendors WHERE id=? AND password=?", (id_, password))
    row = cursor.fetchone()
    
    if row is None:
        # Mostrar un mensaje de error al usuario si los datos no son válidos
        tkinter.messagebox.showerror(title='Login failed', message='Invalid user or password.')
        return # Salir de la función

    # Cerrar la conexión a la base de datos
    conn.close()

    # Cerrar la ventana de login
    window.destroy()

    # Abrir la ventana del módulo de vendedor
    create_vendor_module_window()

def create_vendor_module_window():
    # Aquí puedes crear la ventana con las opciones del módulo de vendedor
    pass

create_vendor_login_window()
