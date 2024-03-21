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
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        subprocess.Popen(["python", "landing.py", username])  # Replace "python" with your Python interpreter if needed
        root.destroy()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials")

# Create the main window
root = tk.Tk()
root.title("Login Page")

# Load the image from desktop
image_path = "./images/Login.png"  # Update the path with your desktop username
image = Image.open(image_path)
image = image.resize((800, 600), Image.LANCZOS)  # Resize image to fit window

# Convert Image object to Tkinter PhotoImage object
photo = ImageTk.PhotoImage(image)

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate position to center window
x = (screen_width - 800) // 2
y = (screen_height - 600) // 2

# Set geometry of the window
root.geometry(f"800x600+{x}+{y}")

# Create a label for the image
image_label = tk.Label(root, image=photo)
image_label.place(x=0, y=0)

# Create and place widgets directly on the main window

username_entry = tk.Entry(root, width=23, font=("Poppins", 12), borderwidth=0, highlightthickness=0)
username_entry.place(relx=0.605, rely=0.32, anchor="w", height=45)

password_entry = tk.Entry(root, show="*", width=16, font=("Poppins", 12), borderwidth=0, highlightthickness=0)
password_entry.place(relx=0.605, rely=0.48, anchor="w", height=44)

login_button = tk.Button(root, text="Login", command=login, bg="#1F75FE", fg="white", width=24, height=2, font=("Helvetica", 12), border=6, borderwidth=0, relief="solid")
login_button.place(relx=0.737, rely=0.65, anchor="center")

# Run the Tkinter event loop
root.mainloop()

# Close the database connection
cursor.close()
db.close()
