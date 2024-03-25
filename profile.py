import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
from PIL import Image, ImageTk
import mysql.connector
import sys

def back():
    subprocess.Popen(["python", "landing.py", username])  # Pass the username back to home.py
    root.destroy()

def open_photos(plotid):
    # Open photos.py with plotid as the first argument and username as the second argument
    subprocess.Popen(["python", "photos.py", str(plotid), username])


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
        mycursor.execute("""
            SELECT p.plotid, p.size, p.price, p.address, r.rating, p.typeofhouse 
            FROM property p 
            LEFT JOIN ratings r ON p.plotid = r.plot_id 
            WHERE p.ownername = %s
        """, (username,))

        records = mycursor.fetchall()

        for i, (plotid, size, price, address, rating, typeofhouse) in enumerate(records, start=1):
            # Insert button to open photos.py with plotid when "Images" text is double-clicked
            properties_table.insert("", "end", values=(plotid, size, price, address, rating, typeofhouse, "Show Details"))

    except Exception as e:
        print(e)
        messagebox.showerror("Error", "Error fetching properties from the database")

    finally:
        mysqldb.close()

def show_favorites():
    # Clear the table
    for item in properties_table.get_children():
        properties_table.delete(item)
    
    # Fetch properties from the favorites table
    # Replace 'your_db_credentials' with your actual database credentials
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="test", database="project")
    mycursor = mysqldb.cursor()

    try:
        # Assuming 'username' is the variable containing the username
        mycursor.execute("""
            SELECT p.plotid, p.size, p.price, p.address, r.rating, p.typeofhouse 
            FROM property p 
            LEFT JOIN ratings r ON p.plotid = r.plot_id 
            INNER JOIN favorite f ON p.plotid = f.favorite_id 
            WHERE f.current_user = %s
        """, (username,))

        records = mycursor.fetchall()

        for i, (plotid, size, price, address, rating, typeofhouse) in enumerate(records, start=1):
            # Insert button to open photos.py with plotid when "Images" text is double-clicked
            properties_table.insert("", "end", values=(plotid, size, price, address, rating, typeofhouse, "Show Details"))

    except Exception as e:
        print(e)
        messagebox.showerror("Error", "Error fetching favorites from the database")

    finally:
        mysqldb.close()



def show_images(event):
    # Get the clicked column
    col_index = properties_table.identify_column(event.x)
    
    # Check if the clicked column corresponds to the "Images" column
    if col_index == '#7':
        # Get the clicked item
        item_clicked = properties_table.identify_row(event.y)
        # Get the values of the clicked item
        values = properties_table.item(item_clicked, 'values')
        if values:
            # Extract the plotid from the clicked item
            print(values)
            plotid = values[0]
            # Open photos.py with plotid as a command line argument
            open_photos(plotid)

if len(sys.argv) > 1:
    username = sys.argv[1]
    print(f"Welcome, {username}!")
else:
    print("No username provided.")
    sys.exit()  # Exit the script if no username is provided

# Create the Tkinter root window
root = tk.Tk()
root.title("Profile Page")
root.geometry("800x600")

# Load the background image
bg_image_path = "./images/Profile1.png"
if os.path.exists(bg_image_path):
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((800, 600), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create a label for the background image
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0)
    bg_label.image = bg_photo  # Keep a reference to the image to prevent garbage collection

    # Lower the background label to the bottom of the stacking order
    bg_label.lower()

    # Center the window on the screen
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (window_width / 2)
    y_coordinate = (screen_height / 2) - (window_height / 2)
    root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))
else:
    print("Background image not found.")

# Label to display "My Properties"
#tk.Label(root, text="My Properties", font=('Helvetica', 16), bg='light blue').pack(pady=10)

# Table to display properties
cols = ('Plot number', 'Size', 'Price', 'Address', 'Rating', 'Type of House', 'Details')  # Updated column name with 'Address'

# Set column widths
col_widths = [110, 110, 110, 110, 110, 110, 110]  # Updated width for the 'Address' column

properties_table = ttk.Treeview(root, columns=cols, show='headings', style="Custom.Treeview")

for col, width in zip(cols, col_widths):
    properties_table.column(col, width=width)

for col in cols:
    properties_table.heading(col, text=col)

#properties_table.pack(pady=10)
properties_table.place(x=20, y=76)

# Bind double-click event to show_images function
properties_table.bind("<Double-1>", show_images)

# Button to go back
back_button = tk.Button(root, text="Back", command=back, width=13, bg="#00FF00", borderwidth=0, highlightthickness=0)
back_button.place(x=26, y=333)

# Button to show properties
show_properties_button = tk.Button(root, text="Show My Properties", command=show_properties, width=18, bg="red", borderwidth=0, highlightthickness=0)
show_properties_button.place(x=157, y=333)

# Button to show favorites
show_favorites_button = tk.Button(root, text="Show Favorites", command=show_favorites, width=18, borderwidth=0, highlightthickness=0, bg="orange")
show_favorites_button.place(x=320, y=333)

# Run the Tkinter event loop
root.mainloop()
