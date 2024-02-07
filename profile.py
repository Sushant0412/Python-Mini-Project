import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import mysql.connector
import sys

def back():
    subprocess.Popen(["python", "home.py", username])  # Pass the username back to home.py
    root.destroy()

def open_photos(plotid):
    # Open photos.py with plotid as a command line argument
    subprocess.Popen(["python", "photos.py", str(plotid)])

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
            # Insert button to open photos.py with plotid when "Images" text is double-clicked
            properties_table.insert("", "end", values=(plotid, size, price, rating, typeofhouse, "Images"))

    except Exception as e:
        print(e)
        messagebox.showerror("Error", "Error fetching properties from the database")

    finally:
        mysqldb.close()

def show_images(event):
    # Get the clicked column
    clicked_column = properties_table.identify_column(event.x)
    
    # Check if the clicked column corresponds to the "Images" column
    if clicked_column == '#6':
        # Get the item clicked
        item_clicked = properties_table.identify_row(event.y)
        # Get the plotid of the item clicked
        plotid = properties_table.item(item_clicked, 'values')[0]
        # Open photos.py with plotid as a command line argument
        open_photos(plotid)

# Check if a username is provided as a command line argument
if len(sys.argv) > 1:
    username = sys.argv[1]
    print(f"Welcome, {username}!")
else:
    print("No username provided.")
    sys.exit(1)  # Exit the script if no username is provided

root = tk.Tk()
root.title("Profile Page")
root.geometry("800x600")

# Label to display "My Properties"
tk.Label(root, text="My Properties", font=('Helvetica', 16)).pack(pady=10)

# Table to display properties
cols = ('Plot number', 'Size', 'Price', 'Rating', 'Type of House', 'Images')  # Updated column name
properties_table = ttk.Treeview(root, columns=cols, show='headings')

# Set column widths
col_widths = [100, 100, 100, 100, 100, 100]  # Adjust widths as needed
for col, width in zip(cols, col_widths):
    properties_table.column(col, width=width)

for col in cols:
    properties_table.heading(col, text=col)

properties_table.pack(pady=10)

# Bind double-click event to show_images function
properties_table.bind("<Double-1>", show_images)

# Button to go back
back_button = tk.Button(root, text="Back", command=back)
back_button.pack(pady=20)

# Button to show properties
show_properties_button = tk.Button(root, text="Show My Properties", command=show_properties)
show_properties_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
