import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttks
import subprocess
import tkinter.messagebox 
import matplotlib.pyplot as plt
import sqlite3
import os
import tkinter.messagebox 

def create_admin_module_window():
    window = ttks.Style(theme='morph').master
    window.title("Admin Module")
    window.geometry('500x300')

    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 20))

    frame = ttk.Frame(window)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    ttk.Label(frame, text="Admin Module", font=('Helvetica', 24)).grid(column=0, row=0, padx=10, pady=10)

    create_seller_button = ttk.Button(frame, text="Create Seller", command=create_seller, style='TButton')
    create_seller_button.grid(column=0, row=1, pady=10)

    generate_report_button = ttk.Button(frame, text="Generate Report", command=generate_report, style='TButton')
    generate_report_button.grid(column=0, row=2,pady=10)

    manage_employees_button = ttk.Button(frame, text="Manage Employees", command=manage_employees, style='TButton')
    manage_employees_button.grid(column=0, row=3,pady=10)

    window.mainloop()

def create_seller():
    try:
        subprocess.run(['python', 'C:\\Users\\PC01A\\Downloads\\MiniProyecto\\AdminModule\\adminCreateVendor.py'])
    except subprocess.CalledProcessError as e:
        tkinter.messagebox.showerror(title='Execution failed', message=f'An error occurred while executing the file: {e}')
        return

def generate_report():

    conn = sqlite3.connect('C:\\Users\\PC01A\\Downloads\\MiniProyecto\\DBMP\\sales.sqlite')
    cursor = conn.cursor()    
    cursor.execute("SELECT date, SUM(total) FROM sales GROUP BY date")
    sales_data = cursor.fetchall()
    conn.close()   
    days = [row[0] for row in sales_data]

    values = [row[1] for row in sales_data]
    fig, ax = plt.subplots(figsize=(10, 6)) 
    ax.bar(days, values, color='#ADD8E6') 
    
    ax.set_title("Sales by day of the month", fontsize=20) 
    ax.set_xlabel("Day", fontsize=16) 
    ax.set_ylabel("Sales", fontsize=16) 

    ax.grid(axis='y', linestyle='--', alpha=0.5)

    
    total_sales = sum(values) 
    ax.annotate(f'Total sales: {total_sales}', xy=(0.8, 0.9), xycoords='figure fraction', fontsize=14) 
    plt.show()

def manage_employees():
    conn = sqlite3.connect('C:\\Users\\PC01A\\Downloads\\MiniProyecto\\DBMP\\vendors.sqlite')
    cursor = conn.cursor()

    # Crear una ventana nueva
    window = tk.Toplevel()
    window.title("Manage Employees")
    window.geometry('500x300')

    # Crear una tabla con los datos de los vendedores
    tree = ttk.Treeview(window, columns=('first_name', 'last_name', 'email', 'password'))
    tree.heading('#0', text='ID')
    tree.heading('first_name', text='First Name')
    tree.heading('last_name', text='Last Name')
    tree.heading('email', text='Email')
    tree.heading('password', text='Password')
    tree.column('#0', width=50)
    tree.column('first_name', width=100)
    tree.column('last_name', width=100)
    tree.column('email', width=100)
    tree.column('password', width=100)
    tree.pack()

    # Llenar la tabla con los datos de la base de datos
    cursor.execute("SELECT * FROM vendors")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert('', 'end', text=row[0], values=(row[1], row[2], row[3], row[4]))

    # Crear botones para modificar o eliminar los vendedores
    # Crear funciones para actualizar o borrar los registros
    def edit_seller():
        # Obtener el ID del vendedor seleccionado
        selected_item = tree.focus()

        # Comprobar si hay algún elemento enfocado
        if selected_item == '':
            # Mostrar un mensaje de advertencia al usuario
            tkinter.messagebox.showwarning(title='No selection', message='Please select a user first.')
            return # Salir de la función

        # Obtener el ID del vendedor
        seller_id = tree.item(selected_item, 'text')

        # Crear una ventana nueva para editar los datos del vendedor
        edit_window = tk.Toplevel()
        edit_window.title("Edit Seller")
        edit_window.geometry('300x200')

        # Crear etiquetas y entradas para los datos del vendedor
        first_name_label = ttk.Label(edit_window, text="First Name:")
        first_name_label.grid(row=0, column=0, padx=10, pady=10)
        first_name_entry = ttk.Entry(edit_window)
        first_name_entry.grid(row=0, column=1, padx=10, pady=10)

        last_name_label = ttk.Label(edit_window, text="Last Name:")
        last_name_label.grid(row=1, column=0, padx=10, pady=10)
        last_name_entry = ttk.Entry(edit_window)
        last_name_entry.grid(row=1, column=1, padx=10, pady=10)

        email_label = ttk.Label(edit_window, text="Email:")
        email_label.grid(row=2, column=0, padx=10, pady=10)
        email_entry = ttk.Entry(edit_window)
        email_entry.grid(row=2, column=1, padx=10, pady=10)

        password_label = ttk.Label(edit_window, text="Password:")
        password_label.grid(row=3, column=0, padx=10, pady=10)
        password_entry = ttk.Entry(edit_window)
        password_entry.grid(row=3, column=1, padx=10, pady=10)

        # Llenar las entradas con los datos actuales del vendedor
        cursor.execute("SELECT * FROM vendors WHERE id=?", (seller_id,))
        row = cursor.fetchone()
        first_name_entry.insert(0, row[1])
        last_name_entry.insert(0, row[2])
        email_entry.insert(0, row[3])
        password_entry.insert(0, row[4])

        # Crear un botón para guardar los cambios
        save_button = ttk.Button(edit_window, text="Save", command=lambda: save_changes())
        save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Crear una función para guardar los cambios en la base de datos
        def save_changes():
            # Obtener los nuevos datos del vendedor
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            email = email_entry.get()
            password = password_entry.get()

            # Actualizar el registro en la base de datos
            cursor.execute("UPDATE vendors SET first_name=?, last_name=?, email=?, password=? WHERE id=?", (first_name, last_name, email, password, seller_id))
            conn.commit()

            # Actualizar la tabla en la ventana principal
            tree.item(selected_item, values=(first_name, last_name, email, password))

            # Cerrar la ventana de edición
            edit_window.destroy()

    def delete_seller():
        # Obtener el ID del vendedor seleccionado
        selected_item = tree.focus()

        # Comprobar si hay algún elemento enfocado
        if selected_item == '':
            # Mostrar un mensaje de advertencia al usuario
            tkinter.messagebox.showwarning(title='No selection', message='Please select a user first.')
            return # Salir de la función

        # Obtener el ID del vendedor
        seller_id = tree.item(selected_item, 'text')

        # Borrar el registro de la base de datos
        cursor.execute("DELETE FROM vendors WHERE id=?", (seller_id,))
        conn.commit()

        # Borrar la fila de la tabla en la ventana principal
        tree.delete(selected_item)
    frame = ttk.Frame(window)
    frame.pack()
    edit_button = ttk.Button(frame, text="Edit", command=edit_seller)
    edit_button.pack(side='left')
    delete_button = ttk.Button(frame, text="Delete", command=delete_seller)
    delete_button.pack(side='right')


    # Cerrar la conexión a la base de datos al cerrar la ventana principal
    window.protocol("WM_DELETE_WINDOW", close_connection)

    def close_connection():
        conn.close()
        window.destroy()

create_admin_module_window()
