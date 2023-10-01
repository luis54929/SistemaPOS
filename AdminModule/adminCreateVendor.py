import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttks
import sqlite3
import random
import string
import tkinter.messagebox 
import smtplib 
from email.message import EmailMessage 
import os # Importamos el módulo os para usar rutas relativas

def create_admin_create_vendor_window():
    window = ttks.Style(theme='morph').master
    window.title("Create Vendor")
    window.geometry('800x600')

    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 20))
    style.configure('TButtonHover', font=('Helvetica', 20), background='#ADD8E6')

    frame = ttk.Frame(window)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    ttk.Label(frame, text="Please enter vendor details:", font=('Helvetica', 24)).grid(column=0, row=0, padx=10, pady=10)

    ttk.Label(frame, text="ID:", font=('Helvetica', 20)).grid(column=0, row=1, padx=10, pady=10)
    id_entry = ttk.Entry(frame)
    id_entry.grid(column=1, row=1)

    ttk.Label(frame, text="First Name:", font=('Helvetica', 20)).grid(column=0, row=2, padx=10, pady=10)
    first_name_entry = ttk.Entry(frame)
    first_name_entry.grid(column=1, row=2)

    ttk.Label(frame, text="Last Name:", font=('Helvetica', 20)).grid(column=0, row=3, padx=10, pady=10)
    last_name_entry = ttk.Entry(frame)
    last_name_entry.grid(column=1, row=3)

    ttk.Label(frame, text="Email:", font=('Helvetica', 20)).grid(column=0, row=4, padx=10, pady=10) # Añadimos un campo para el correo electrónico del vendedor
    email_entry = ttk.Entry(frame)
    email_entry.grid(column=1, row=4)

    create_button = ttk.Button(frame, text="Create", command=lambda: create_vendor(id_entry.get(), first_name_entry.get(), last_name_entry.get(), email_entry.get()), style='TButton')
    create_button.grid(column=1, row=5, pady=20)

    window.mainloop()

def on_enter(event):
    event.widget.configure(style='TButtonHover') # Cambiamos el estilo del botón a TButtonHover

def on_leave(event):
    event.widget.configure(style='TButton') # Cambiamos el estilo del botón a TButton

def create_vendor(id_, first_name, last_name, email):
    password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(8)) # Añadimos caracteres especiales a la contraseña
    
    conn = sqlite3.connect('C:\\Users\\PC01A\\Downloads\\MiniProyecto\\DBMP\\vendors.sqlite')
    cursor = conn.cursor()

    
    cursor.execute("CREATE TABLE IF NOT EXISTS vendors (id INTEGER PRIMARY KEY NOT NULL, first_name TEXT NOT NULL, last_name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL)") # Añadimos restricciones e índices a los campos de la tabla

   
    try:
        cursor.execute("INSERT INTO vendors (id, first_name, last_name, email, password) VALUES (?, ?, ?, ?, ?)", (id_, first_name, last_name, email, password)) # Intentamos insertar los datos del vendedor en la tabla
        conn.commit() # Confirmamos los cambios en la base de datos
    except sqlite3.IntegrityError as e: # Capturamos la excepción si ocurre algún error al insertar los datos
        tkinter.messagebox.showerror(title='Vendor creation failed', message=f'An error occurred while creating the vendor: {e}') # Mostramos un mensaje de error al usuario
        return # Salimos de la función
    
    conn.close() # Cerramos la conexión a la base de datos
    message = EmailMessage()
    message['Subject'] = 'Welcome to the POS system'
    message['From'] = 'SistemaPosJave@gmx.com'
    message['To'] = email
    message.set_content(f'Hello {first_name} {last_name},\n\nYou have been registered as a vendor in the POS system of XYZ company.\n\nYour access code is: {password}\n\nPlease use this code to log in to the system and start selling.\n\nThank you for your service.\n\nSincerely,\n\nThe admin team.')
    message.set_charset('utf-8') # Indicamos el formato de codificación del mensaje
    correo_electronico= "SistemaPosJave@gmx.com"
    password_correo = "Javeriana123*"
    server = smtplib.SMTP("mail.gmx.com", 587)
    print("Comenzo el Envio")
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(correo_electronico,password_correo)
    server.send_message(message)
    server.quit() # Cerramos la conexión al servidor de correo
    tkinter.messagebox.showinfo(title='Vendor created', message=f'You have successfully created a vendor with the following details:\n\nID: {id_}\nFirst name: {first_name}\nLast name: {last_name}\nEmail: {email}\nAccess code: {password}') # Usamos un salto de línea para separar las líneas del mensaje

create_admin_create_vendor_window()
