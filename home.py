import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import sys
from tkinter import Scrollbar
from PIL import Image, ImageTk
import subprocess

username = "None"

if len(sys.argv) > 1:
    username = sys.argv[1]
    print(f"Welcome, {username}!")
else:
    print("No username provided.")

root = tk.Tk(className=' Real Estate Management System')
window_width = 800
window_height = 600

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_coordinate = (screen_width/2) - (window_width/2)
y_coordinate = (screen_height/2) - (window_height/2)

root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))
root.configure(bg='light blue')

global e1
global e2
global e3
global e4
global e5
global e6

tk.Label(root, text="Plot number").place(x=10, y=20)
Label(root, text="Owner Name").place(x=10, y=50)
Label(root, text="Size").place(x=10, y=80)
Label(root, text="Price").place(x=10, y=110)
Label(root, text="Rating").place(x=10, y=140)
Label(root, text="Type of House").place(x=10, y=170)
Label(root, text=username).place(x=680, y=80)

e1 = Entry(root)
e1.place(x=140, y=20)

e2 = Entry(root)
e2.insert(0, username)  # Set owner's name as the username
e2.config(state='disabled')  # Make it read-only
e2.place(x=140, y=50)

e3 = Entry(root)
e3.place(x=140, y=80)

e4 = Entry(root)
e4.place(x=140, y=110)

e5 = Entry(root)
e5.place(x=140, y=140)

e6 = Entry(root)
e6.place(x=140, y=170)


def Add():
    studid = e1.get()
    studname = e2.get()
    size = e3.get()
    price = e4.get()
    rating = e5.get()
    typeofhouse = e6.get()

    # Check if all fields are filled
    if not studid or not studname or not size or not price or not rating or not typeofhouse:
        messagebox.showerror("Error", "All fields are compulsory!")
        return

    mysqldb = mysql.connector.connect(host="localhost", user="root", password="test", database="project")
    mycursor = mysqldb.cursor()

    try:
        sql = "INSERT INTO property (plotid, ownername, size, price, rating, typeofhouse) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (studid, studname, size, price, rating, typeofhouse)
        mycursor.execute(sql, val)
        mysqldb.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("", "Plot added!")
        clear_entries()
        listBox.delete(*listBox.get_children())
        show()

    except Exception as e:
        print(e)
        mysqldb.rollback()

    finally:
        mysqldb.close()


def update():
    plotid = e1.get()
    size = e3.get()
    price = e4.get()
    rating = e5.get()
    typeofhouse = e6.get()

    # Check if plotid is filled
    if not plotid:
        messagebox.showerror("Error", "Plot ID is compulsory!")
        return
    
    # Connect to the database
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="test", database="project")
    mycursor = mysqldb.cursor()

    try:
        # Fetch the existing values from the database for the provided plotid and ownername
        mycursor.execute("SELECT size, price, rating, typeofhouse FROM property WHERE plotid = %s AND ownername = %s", (plotid, username))
        record = mycursor.fetchone()

        if not record:
            messagebox.showerror("Error", "You are not the owner of this property.")
            return

        # Update the fields that are filled, keep the rest unchanged
        if size:
            record[0] = size
        if price:
            record[1] = price
        if rating:
            record[2] = rating
        if typeofhouse:
            record[3] = typeofhouse

        # Perform the update operation
        sql = "UPDATE property SET size = %s, price = %s, rating = %s, typeofhouse = %s WHERE plotid = %s AND ownername = %s"
        val = (record[0], record[1], record[2], record[3], plotid, username)
        mycursor.execute(sql, val)
        mysqldb.commit()
        messagebox.showinfo("", "Plot Updated")
        clear_entries()
        listBox.delete(*listBox.get_children())
        show()

    except mysql.connector.Error as err:
        print("MySQL error:", err)
        mysqldb.rollback()
        messagebox.showerror("Error", "Failed to update plot details. Please check your input and try again.")

    finally:
        mysqldb.close()





def search():
    # Get the ID entered by the user
    search_id = e1.get()

    # Check if the ID is provided
    if not search_id:
        messagebox.showerror("Error", "Please enter an ID to search for.")
        return

    # Connect to the database
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="test", database="project")
    mycursor = mysqldb.cursor()

    try:
        # Execute the SQL query to fetch properties based on the provided ID
        mycursor.execute("SELECT plotid, ownername, size, price, rating, typeofhouse FROM property WHERE plotid = %s", (search_id,))
        records = mycursor.fetchall()

        # Clear existing items in the Listbox
        listBox.delete(*listBox.get_children())

        # Populate the Listbox with the fetched records
        for i, (plotid, ownername, size, price, rating, typeofhouse) in enumerate(records, start=1):
            listBox.insert("", "end", values=(plotid, ownername, size, price, rating, typeofhouse))

    except Exception as e:
        print(e)
        messagebox.showerror("Error", "Error fetching properties from the database")

    finally:
        # Close the database connection
        mysqldb.close()


def delete():
    studid = e1.get()

    mysqldb = mysql.connector.connect(host="localhost", user="root", password="test", database="project")
    mycursor = mysqldb.cursor()

    try:
        sql = "DELETE FROM property WHERE plotid = %s AND ownername = %s"
        val = (studid, username)
        mycursor.execute(sql, val)
        mysqldb.commit()
        messagebox.showinfo("", "Plot deleted!")
        clear_entries()
        listBox.delete(*listBox.get_children())
        show()

    except Exception as e:
        print(e)
        mysqldb.rollback()

    finally:
        mysqldb.close()


def GetValue(event):
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    e5.delete(0, END)
    e6.delete(0, END)
    row_id = listBox.selection()[0]
    select = listBox.set(row_id)
    e1.insert(0, select['plotid'])
    e3.insert(0, select['size'])
    e4.insert(0, select['price'])
    e5.insert(0, select['rating'])
    e6.insert(0, select['typeofhouse'])


def show():
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="test", database="project")
    mycursor = mysqldb.cursor()

    try:
        mycursor.execute("SELECT plotid, ownername, size, price, rating, typeofhouse FROM property")
        records = mycursor.fetchall()

        for i, (plotid, ownername, size, price, rating, typeofhouse) in enumerate(records, start=1):
            listBox.insert("", "end", values=(plotid, ownername, size, price, rating, typeofhouse))

    except Exception as e:
        print(e)
        messagebox.showerror("Error", "Error fetching properties from the database")

    finally:
        mysqldb.close()


def profile():
    subprocess.Popen(["python", "profile.py", username])
    root.destroy()
    # Replace "python" with your Python interpreter if needed


def logout():
    root.destroy()
    subprocess.Popen(["python", "login.py"])  # Replace "python" with your Python interpreter if needed

def refresh():
    clear_entries()
    listBox.delete(*listBox.get_children())
    show()

def clear_entries():
    e1.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    e5.delete(0, END)
    e6.delete(0, END)
    e1.focus_set()

Button(root, text="Add", command=Add, height=3, width=13).place(x=30, y=210)
Button(root, text="Update", command=update, height=3, width=13).place(x=140, y=210)
Button(root, text="Delete", command=delete, height=3, width=13).place(x=250, y=210)
Button(root, text="Search", command=search, height=3, width=13).place(x=360, y=210)
Button(root, text="Refresh", command=refresh, height=3,width=13).place(x=470, y=210)
Button(root, text="Logout", command=logout, height=3, width=13).place(x=580, y=210)
Button(root, text="Profile", command=profile,height=3, width=13).place(x=650, y=20)

cols = ('Plot number', 'Owner Name', 'Size', 'Price', 'Rating', 'Type of House')
listBox = ttk.Treeview(root, columns=cols, show='headings')

listBox_width = 780
hsb_width = 776

for col in cols:
    listBox.heading(col, text=col)
    listBox.column(col, anchor='center')  # Add this line to center align the column data
    listBox.grid(row=1, column=0, columnspan=2)
    listBox.place(x=10, y=280, width=listBox_width, height=210)

hsb = ttk.Scrollbar(root, orient="horizontal", command=listBox.xview)
hsb.place(x=12, y=472, width=hsb_width)
listBox.configure(xscrollcommand=hsb.set)

show()
listBox.bind('<Double-Button-1>', GetValue)

root.mainloop()
