import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from PIL import Image, ImageTk
import subprocess

root = Tk(className=' Real Estate Management System')
root.geometry("800x500")
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

e1 = Entry(root)
e1.place(x=140, y=20)

e2 = Entry(root)
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

    mysqldb = mysql.connector.connect(host="localhost", user="root", password="test", database="project")
    mycursor = mysqldb.cursor()

    try:
        sql = "INSERT INTO property (plotid, ownername, size, price, rating, typeofhouse) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (studid, studname, size, price, rating, typeofhouse)
        mycursor.execute(sql, val)
        mysqldb.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("", "Plot added!")
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e5.delete(0, END)
        e6.delete(0, END)
        e1.focus_set()

    except Exception as e:
        print(e)
        mysqldb.rollback()
        mysqldb.close()


def update():
    studid = e1.get()
    studname = e2.get()
    size = e3.get()
    price = e4.get()
    rating = e5.get()
    typeofhouse = e6.get()
    
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="test", database="project")
    mycursor = mysqldb.cursor()

    try:
        sql = "UPDATE property SET ownername = %s, size = %s, price = %s, rating = %s, typeofhouse = %s WHERE plotid = %s"
        val = (studname, size, price, rating, typeofhouse, studid)
        mycursor.execute(sql, val)
        mysqldb.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("", "Plot Updated")

        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e5.delete(0, END)
        e6.delete(0, END)
        e1.focus_set()

    except Exception as e:
        print(e)
        mysqldb.rollback()
        mysqldb.close()


def search():
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="test", database="project")
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT plotid, ownername, size, price, rating, typeofhouse FROM property")
    records = mycursor.fetchall()

    for i, (plotid, ownername, size, price, rating, typeofhouse) in enumerate(records, start=1):
        msg = f"Plot number: {plotid}\nOwner name: {ownername}\nSize: {size}\nPrice: {price}\nRating: {rating}\nType of House: {typeofhouse}"
        messagebox.showinfo("Plot Details", msg)

    mysqldb.close()


def delete():
    studid = e1.get()

    mysqldb = mysql.connector.connect(host="localhost", user="root", password="test", database="project")
    mycursor = mysqldb.cursor()

    try:
        sql = "DELETE FROM property WHERE plotid = %s"
        val = (studid,)
        mycursor.execute(sql, val)
        mysqldb.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("", "Plot deleted!")

        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e5.delete(0, END)
        e6.delete(0, END)
        e1.focus_set()

    except Exception as e:
        print(e)
        mysqldb.rollback()
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
    e2.insert(0, select['ownername'])
    e3.insert(0, select['size'])
    e4.insert(0, select['price'])
    e5.insert(0, select['rating'])
    e6.insert(0, select['typeofhouse'])


def show():
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="test", database="project")
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT plotid, ownername, size, price, rating, typeofhouse FROM property")
    records = mycursor.fetchall()

    for i, (plotid, ownername, size, price, rating, typeofhouse) in enumerate(records, start=1):
        listBox.insert("", "end", values=(plotid, ownername, size, price, rating, typeofhouse))

    mysqldb.close()


def logout():
    root.destroy()
    subprocess.Popen(["python", "login.py"])  # Replace "python" with your Python interpreter if needed


Button(root, text="Add", command=Add, height=3, width=13).place(x=30, y=210)
Button(root, text="Update", command=update, height=3, width=13).place(x=140, y=210)
Button(root, text="Delete", command=delete, height=3, width=13).place(x=250, y=210)
Button(root, text="Search", command=search, height=3, width=13).place(x=360, y=210)
Button(root, text="Logout", command=logout, height=3, width=13).place(x=470, y=210)  # Added Logout button

cols = ('Plot number', 'Owner Name', 'Size', 'Price', 'Rating', 'Type of House')
listBox = ttk.Treeview(root, columns=cols, show='headings')

for col in cols:
    listBox.heading(col, text=col)
    listBox.grid(row=1, column=0, columnspan=2)
    listBox.place(x=1, y=280)

show()
listBox.bind('<Double-Button-1>', GetValue)

root.mainloop()
