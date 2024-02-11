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
        subprocess.Popen(["python", "home.py", username])  # Replace "python" with your Python interpreter if needed
        root.destroy()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials")

# Create the main window
root = tk.Tk()
root.title("Login Page")

# Load the image
image = Image.open("./images/loginBg.webp")  # Change the file name accordingly
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

# Create a frame for the right side (for login box)
right_frame = tk.Frame(root, bg="#d8dbd8", bd=2, relief="solid")  # Add border to frame
right_frame.place(relx=0.8, rely=0.5, anchor="center", relwidth=0.3, relheight=0.5)

# Create and place widgets inside the right frame
username_label = tk.Label(right_frame, text="Username:", bg="#d8dbd8", fg="black", font=("Helvetica", 12))
username_label.place(relx=0.05, rely=0.2, anchor="w")

username_frame = tk.Frame(right_frame, bg="#d8dbd8")  # Frame for padding
username_frame.place(relx=0.4, rely=0.2, anchor="w")
username_entry = tk.Entry(username_frame, width=13, font=("Helvetica", 12))
username_entry.pack(padx=5, pady=5)  # Add padding

password_label = tk.Label(right_frame, text="Password:", bg="#d8dbd8", fg="black", font=("Helvetica", 12))
password_label.place(relx=0.05, rely=0.4, anchor="w")

password_frame = tk.Frame(right_frame, bg="#d8dbd8")  # Frame for padding
password_frame.place(relx=0.4, rely=0.4, anchor="w")
password_entry = tk.Entry(password_frame, show="*", width=13, font=("Helvetica", 12))
password_entry.pack(padx=5, pady=5)  # Add padding

login_button = tk.Button(right_frame, text="Login", command=login, bg="green", fg="white", width=20, font=("Helvetica", 12))
login_button.place(relx=0.5, rely=0.7, anchor="center")

# Run the Tkinter event loop
root.mainloop()

# Close the database connection
cursor.close()
db.close()
