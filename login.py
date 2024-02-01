import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
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
root.geometry("800x600")

# Center the Tkinter window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - 800) / 2
y_coordinate = (screen_height - 600) / 2
root.geometry("+%d+%d" % (int(x_coordinate), int(y_coordinate)))

# Set background image
path = "./images/introImage.jpg"
img = Image.open(path)
img = img.resize((800, 600), Image.LANCZOS)
background_image = ImageTk.PhotoImage(img)
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Create and place widgets
username_label = tk.Label(root, text="Username:", bg="white")
username_entry = tk.Entry(root)

password_label = tk.Label(root, text="Password:", bg="white")
password_entry = tk.Entry(root, show="*")

login_button = tk.Button(root, text="Login", command=login)

# Use the grid layout manager
username_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")
username_entry.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")

password_label.grid(row=2, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")
password_entry.grid(row=3, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")

login_button.grid(row=4, column=0, columnspan=2, pady=10)

# Run the Tkinter event loop
root.mainloop()

# Close the database connection
cursor.close()
db.close()
