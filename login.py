import tkinter as tk
from tkinter import messagebox
import subprocess
import mysql.connector

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="test",
    database="project"
)

cursor = db.cursor()

def login():
    username = username_entry.get()
    password = password_entry.get()

    # Check if the user exists
    cursor.execute('SELECT * FROM login WHERE user=%s AND pass=%s', (username, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
        # Add code to open home.py here
        subprocess.Popen(["python", "home.py"])  # Replace "python" with your Python interpreter if needed
        root.destroy()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials")

# Create the main window
root = tk.Tk()
root.title("Login Page")

# Create and place widgets
username_label = tk.Label(root, text="Username:")
username_entry = tk.Entry(root)

password_label = tk.Label(root, text="Password:")
password_entry = tk.Entry(root, show="*")

login_button = tk.Button(root, text="Login", command=login)

# Use the grid layout manager
username_label.grid(row=0, column=0, padx=10, pady=10)
username_entry.grid(row=0, column=1, padx=10, pady=10)

password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry.grid(row=1, column=1, padx=10, pady=10)

login_button.grid(row=2, column=0, columnspan=2, pady=10)

# Run the Tkinter event loop
root.mainloop()

# Close the database connection
cursor.close()
db.close()
