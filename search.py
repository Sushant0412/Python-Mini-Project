import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import sys
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import subprocess

username = "None"

if len(sys.argv) > 1:
    username = sys.argv[1]
    print(f"Welcome, {username}!")
else:
    print("No username provided.")

root = tk.Tk(className=' Real Estate Management System')

# Set window dimensions and position
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width / 2) - (window_width / 2)
y_coordinate = (screen_height / 2) - (window_height / 2)
root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

# Load and resize the background image
bg_image = Image.open("./images/Home.png")
bg_image = bg_image.resize((window_width, window_height), Image.LANCZOS)  # Use Lanczos resampling
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a Label to display the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

root.configure(bg='light blue')

global e1
global e2
global e3
global e4
global e5
global e6

# tk.Label(root, text="Plot number").place(x=10, y=20)
# # tk.Label(root, text="Owner Name").place(x=290, y=20)
# tk.Label(root, text="Size").place(x=10, y=80)
# tk.Label(root, text="Price").place(x=10, y=110)
# tk.Label(root, text="Address").place(x=10, y=140)
# tk.Label(root, text="Type of House").place(x=10, y=170)
tk.Label(root, text=username, width=5).place(x=710, y=117)
# tk.Label(root, text="City").place(x=10, y=50)

e1 = tk.Entry(root, borderwidth=0, highlightthickness=0)
e1.place(x=165, y=82)

e2 = tk.Entry(root)
e2.insert(0, username)  # Set owner's name as the username
e2.config(state='disabled')  # Make it read-only

e3 = tk.Entry(root, borderwidth=0, highlightthickness=0)
e3.place(x=165, y=122)

e4 = tk.Entry(root, borderwidth=0, highlightthickness=0)
e4.place(x=165, y=163)

e5 = tk.Entry(root, borderwidth=0, highlightthickness=0)
e5.place(x=435, y=124)

e6 = tk.Entry(root, borderwidth=0, highlightthickness=0)
e6.place(x=435, y=164)

e7 = tk.Entry(root, borderwidth=0, highlightthickness=0)
e7.place(x=435, y=80)


def Add():
    studid = e1.get()
    studname = e2.get()
    size = e3.get()
    price = e4.get()
    address = e5.get()
    typeofhouse = e6.get()
    city = e7.get()  # Add city attribute

    # Check if all fields are filled
    if not studid or not studname or not size or not price or not address or not typeofhouse or not city:
        messagebox.showerror("Error", "All fields are compulsory!")
        return

    try:
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="test", database="project")
        mycursor = mysqldb.cursor()

        sql = "INSERT INTO property (plotid, ownername, size, price, address, typeofhouse, city) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (studid, studname, size, price, address, typeofhouse, city)
        mycursor.execute(sql, val)
        mysqldb.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("", "Plot added!")
        clear_entries()
        listBox.delete(*listBox.get_children())
        show()

    except mysql.connector.Error as err:
        # Handle specific MySQL errors
        messagebox.showerror("MySQL Error", f"Error: {err.msg}")

    except Exception as e:
        # Handle other exceptions
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

    finally:
        # Close the database connection
        if 'mysqldb' in locals() and mysqldb.is_connected():
            mycursor.close()
            mysqldb.close()


def update():
    studid = e1.get()
    studname = e2.get()
    size = e3.get()
    price = e4.get()
    address = e5.get()
    typeofhouse = e6.get()
    city = e7.get()  # Add city attribute

    # Check if all fields are filled
    if not studid or not studname or not size or not price or not address or not typeofhouse or not city:
        messagebox.showerror("Error", "All fields are compulsory!")
        return
    
    # Check if the property ownername matches the current username
    if studname != username:
        messagebox.showerror("Error", "You are not authorized to update this property.")
        return
    
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="test", database="project")
    mycursor = mysqldb.cursor()

    try:
        sql = "UPDATE property SET size = %s, price = %s, address = %s, typeofhouse = %s, city = %s, plotid = %s WHERE ownername = %s"
        val = (size, price, address, typeofhouse, city, studid, studname)
        mycursor.execute(sql, val)
        mysqldb.commit()
        messagebox.showinfo("", "Plot Updated")
        clear_entries()
        listBox.delete(*listBox.get_children())
        show()

    except Exception as e:
        print(e)
        mysqldb.rollback()

    finally:
        mysqldb.close()


def search():
    # Get the city criteria entered by the user
    city_criteria = e7.get()  # City search criteria

    # Check if the city criteria is provided
    if not city_criteria:
        messagebox.showerror("Error", "Please enter a city to search for.")
        return

    # Connect to the database
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="test", database="project")
    mycursor = mysqldb.cursor()

    try:
        # Define the SQL query to fetch properties based on the provided city criteria
        sql = """
            SELECT p.plotid, p.ownername, p.size, p.price, p.address, p.typeofhouse, r.rating 
            FROM property p 
            LEFT JOIN ratings r ON p.plotid = r.plot_id 
            WHERE p.city = %s
        """

        # Execute the SQL query with the city criteria
        mycursor.execute(sql, (city_criteria,))
        records = mycursor.fetchall()

        # Clear existing items in the Listbox
        listBox.delete(*listBox.get_children())

        # Populate the Listbox with the fetched records
        for i, (plotid, ownername, size, price, address, typeofhouse, rating) in enumerate(records, start=1):
            listBox.insert("", "end", values=(plotid, ownername, size, price, address, typeofhouse, rating, "Show Details"))

    except mysql.connector.Error as err:
        print("MySQL Error:", err.msg)
        messagebox.showerror("Error", f"MySQL Error: {err.msg}")

    except Exception as e:
        print("Exception:", e)
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

    finally:
        # Close the database connection
        mysqldb.close()

def delete():
    global id_value
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="test", database="project")
    mycursor = mysqldb.cursor()

    try:
        # Fetch the plotid using id_value
        studid = e1.get()
        mycursor.execute("SELECT plotid FROM property WHERE plotid = %s", (studid,))
        result = mycursor.fetchone()
        plotid = result[0] if result else None

        # Check if the plotid matches the current user and ownername is the current username
        mycursor.execute("SELECT ownername FROM property WHERE plotid = %s", (studid,))
        result = mycursor.fetchone()
        ownername = result[0] if result else None
        
        if plotid and ownername == username:
            # Delete from property table
            sql_property = "DELETE FROM property WHERE plotid = %s"
            val_property = (plotid,)
            mycursor.execute(sql_property, val_property)

            # Delete from ratings table if exists
            sql_ratings = "DELETE FROM ratings WHERE plot_id = %s"
            val_ratings = (plotid,)
            mycursor.execute(sql_ratings, val_ratings)

            # Delete from favorites table if exists
            sql_favorites = "DELETE FROM favorite WHERE favorite_id = %s"
            val_favorites = (plotid,)
            mycursor.execute(sql_favorites, val_favorites)

            mysqldb.commit()
            messagebox.showinfo("", "Plot deleted!")
            clear_entries()
            listBox.delete(*listBox.get_children())
            show()
        else:
            messagebox.showerror("", "You are not authorized to delete this plot.")

    except Exception as e:
        print(e)
        mysqldb.rollback()

    finally:
        mysqldb.close()


def GetValue(event):
    global id_value
    e1.delete(0, tk.END)
    e2.delete(0, tk.END)
    e3.delete(0, tk.END)
    e4.delete(0, tk.END)
    e5.delete(0, tk.END)
    e6.delete(0, tk.END)
    row_id = listBox.selection()[0]
    column_id = listBox.identify_column(event.x)
    
    if column_id == '#8':  # Check if double-clicked column is the "Details" column
        select = listBox.item(row_id)
        id_value = select['values'][0]  # Set the id_value to the selected plotid
        plot_id = select['values'][0]
        subprocess.Popen(["python", "photos.py", str(plot_id), username])
    
    elif column_id == '#2':  # Check if double-clicked column is the "Owner Name" column
        select = listBox.item(row_id)
        id_value = select['values'][0]  # Set the id_value to the selected plotid
        prop_owner = select['values'][1]
        # Connect to the database
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="test", database="project")
        mycursor = mysqldb.cursor()

        try:
            # Check if the property is already in the favorites table
            mycursor.execute("SELECT * FROM favorite WHERE favorite_id = %s AND ownername = %s", (id_value, prop_owner))
            result = mycursor.fetchone()

            if result:
                # If property is already in favorites, remove it from favorites
                sql = "DELETE FROM favorite WHERE favorite_id = %s AND ownername = %s"
                val = (id_value, prop_owner)
                mycursor.execute(sql, val)
                mysqldb.commit()
                messagebox.showinfo("", "Property removed from favorites!")
            else:
                # If property is not in favorites, add it to favorites
                sql = "INSERT INTO favorite (favorite_id, ownername, `current_user`) VALUES (%s, %s, %s)"
                val = (id_value, prop_owner, username)
                mycursor.execute(sql, val)

                mysqldb.commit()
                messagebox.showinfo("", "Property added to favorites!")
            
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "An error occurred")

        finally:
            mysqldb.close()
    
    else:
        select = listBox.item(row_id)
        e1.insert(0, select['values'][0])
        e2.insert(0, select['values'][1])
        e3.insert(0, select['values'][2])
        e4.insert(0, select['values'][3])
        e5.insert(0, select['values'][4])
        e6.insert(0, select['values'][5])


from datetime import datetime, timedelta
import threading  # Import threading module for handling the price incrementation in a separate thread
import time
# Define a global variable to store the refresh interval in seconds
refresh_interval = 31536000  # 2 minutes

def increment_prices():
    # Connect to the database
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="test", database="project")
    mycursor = mysqldb.cursor()

    try:
        while True:
            # Fetch all properties from the database
            mycursor.execute("SELECT plotid, price, lastUpdated FROM property")
            records = mycursor.fetchall()

            current_date = datetime.now()

            for plotid, price, last_updated in records:
                difference_seconds = (current_date - last_updated).total_seconds()

                if difference_seconds >= refresh_interval:
                    # Increment the price by 7%
                    new_price = price + (price * 0.07)
                    # Update the price and lastUpdated in the database
                    update_query = "UPDATE property SET price = %s, lastUpdated = %s WHERE plotid = %s"
                    mycursor.execute(update_query, (new_price, current_date, plotid))
                    mysqldb.commit()  # Commit the transaction

            # Sleep for the refresh interval before incrementing prices again
            time.sleep(refresh_interval)

    except Exception as e:
        print(e)

    finally:
        mysqldb.close()

# Start the price incrementation thread
price_thread = threading.Thread(target=increment_prices)
price_thread.daemon = True  # Set the thread as a daemon thread to stop automatically when the main thread exits
price_thread.start()

# Function to display properties in the GUI
def show():
    try:
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="test", database="project")
        mycursor = mysqldb.cursor()

        # Fetch properties from the database
        mycursor.execute("SELECT p.plotid, p.ownername, p.size, p.price, p.address, p.typeofhouse, r.rating FROM property p LEFT JOIN ratings r ON p.plotid = r.plot_id")
        records = mycursor.fetchall()

        for i, (plotid, ownername, size, price, address, typeofhouse, rating) in enumerate(records, start=1):
            listBox.insert("", "end", values=(plotid, ownername, size, price, address, typeofhouse, rating, "Show Details"))

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
    subprocess.Popen(["python", "landing.py", username])  # Replace "python" with your Python interpreter if needed

def refresh():
    clear_entries()
    listBox.delete(*listBox.get_children())
    show()

def clear_entries():
    e1.delete(0, tk.END)
    e3.delete(0, tk.END)
    e4.delete(0, tk.END)
    e5.delete(0, tk.END)
    e6.delete(0, tk.END)
    e7.delete(0, tk.END)
    e1.focus_set()

tk.Button(root, text="Search", command=search, font=("Arial", 12), height=2, width=11, bd=0, relief=tk.FLAT, bg="green", fg="white").place(x=80, y=230)
tk.Button(root, text="Update", command=update, font=("Arial", 12), height=2, width=11, bd=0, relief=tk.FLAT, bg="orange", fg="white").place(x=210, y=230)
tk.Button(root, text="Refresh", command=refresh, font=("Arial", 12), height=2, width=11, bd=0, relief=tk.FLAT, bg="blue", fg="white").place(x=340, y=230)
tk.Button(root, text="Back", command=logout, font=("Arial", 12), height=2, width=11, bd=0, relief=tk.FLAT, bg="red", fg="white").place(x=470, y=230)
tk.Button(root, text="View Profile", command=profile,height=1, width=10).place(x=668, y=145)

cols = ('Plot number', 'Owner Name', 'Size', 'Price', 'Address', 'Type of House','Rating', 'Details')
listBox = ttk.Treeview(root, columns=cols, show='headings')

listBox_width = 760
hsb_width = 760

for col in cols:
    listBox.heading(col, text=col)
    listBox.column(col, anchor='center')  # Add this line to center align the column data

listBox.place(x=20, y=300, width=listBox_width, height=260)

hsb = ttk.Scrollbar(root, orient="horizontal", command=listBox.xview)
hsb.place(x=20, y=564, width=hsb_width)
listBox.configure(xscrollcommand=hsb.set)

show()
listBox.bind('<Double-Button-1>', GetValue)

root.mainloop()

