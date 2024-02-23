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
    subprocess.Popen(["python", "photos.py", username, str(plotid)])

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
            plotid = values[0]
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

# Center the window on the screen
window_width = 800
window_height = 600

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_coordinate = (screen_width / 2) - (window_width / 2)
y_coordinate = (screen_height / 2) - (window_height / 2)

root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

# Configure background color
root.configure(bg='light blue')

# Add a style
style = ttk.Style(root)
style.theme_use("clam")  # You can change the theme as needed

# Label to display "My Properties"
tk.Label(root, text="My Properties", font=('Helvetica', 16), bg='light blue').pack(pady=10)

# Table to display properties
cols = ('Plot number', 'Size', 'Price', 'Address', 'Rating', 'Type of House', 'Details')  # Updated column name with 'Address'

# Set column widths
col_widths = [110, 110, 110, 110, 110, 110, 110]  # Updated width for the 'Address' column

properties_table = ttk.Treeview(root, columns=cols, show='headings', style="Custom.Treeview")

for col, width in zip(cols, col_widths):
    properties_table.column(col, width=width)

for col in cols:
    properties_table.heading(col, text=col)

properties_table.pack(pady=10)

# Bind double-click event to show_images function
properties_table.bind("<Double-1>", show_images)

# Button to go back
back_button = tk.Button(root, text="Back", command=back, width=10)
back_button.pack(pady=20)

# Button to show properties
show_properties_button = tk.Button(root, text="Show My Properties", command=show_properties, width=20)
show_properties_button.pack(pady=10)

# Button to show favorites
show_favorites_button = tk.Button(root, text="Show Favorites", command=show_favorites, width=20)
show_favorites_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
