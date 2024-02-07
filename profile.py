import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import mysql.connector
import sys

def back():
    subprocess.Popen(["python", "home.py", username])  # Pass the username back to home.py
    root.destroy()

def show_properties():
    # Clear the table
    for item in properties_table.get_children():
        properties_table.delete(item)
    
    # Fetch properties owned by the user from the database and display in the table
    # Replace 'your_db_credentials' with your actual database credentials
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="test", database="project")
    mycursor = mysqldb.cursor()

    try:
        # Assuming 'username' is the variable containing the username
        mycursor.execute("SELECT plotid, size, price, rating, typeofhouse FROM property WHERE ownername=%s", (username,))
        records = mycursor.fetchall()

        for i, (plotid, size, price, rating, typeofhouse) in enumerate(records, start=1):
            # Insert button to open photos.py with plotid
            button = tk.Button(root, text="View Images", command=lambda plotid=plotid: show_images(plotid))
            properties_table.insert("", "end", values=(plotid, size, price, rating, typeofhouse, button))

    except Exception as e:
        print(e)
        messagebox.showerror("Error", "Error fetching properties from the database")

    finally:
        mysqldb.close()

def show_images(plotid):
    # Open photos.py with plotid as a command line argument
    subprocess.Popen(["python", "photos.py", str(plotid)])

# Check if a username is provided as a command line argument
if len(sys.argv) > 1:
    username = sys.argv[1]
    print(f"Welcome, {username}!")
else:
    print("No username provided.")
    sys.exit(1)  # Exit the script if no username is provided

root = tk.Tk()
root.title("Profile Page")

# Label to display "My Properties"
tk.Label(root, text="My Properties", font=('Helvetica', 16)).pack(pady=10)

# Table to display properties
cols = ('Plot number', 'Size', 'Price', 'Rating', 'Type of House', 'Image')  # Updated column name
properties_table = ttk.Treeview(root, columns=cols, show='headings')

for col in cols:
    properties_table.heading(col, text=col)

properties_table.pack(pady=10)

# Button to go back
back_button = tk.Button(root, text="Back", command=back)
back_button.pack(pady=20)

# Button to show properties
show_properties_button = tk.Button(root, text="Show My Properties", command=show_properties)
show_properties_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
