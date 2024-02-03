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
        # print(username)
        subprocess.Popen(["python", "home.py", username])  # Replace "python" with your Python interpreter if needed
        root.destroy()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials")

# Create the main window
root = tk.Tk()
root.title("Login Page")
root.geometry("800x600")
peach_color = "#f6b092"
root.configure(bg=peach_color)
# Center the Tkinter window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - 800) / 2
y_coordinate = (screen_height - 600) / 2
root.geometry("+%d+%d" % (int(x_coordinate), int(y_coordinate)))

# Set background image


# Create and place widgets
container_label = tk.Label(root, bg="#214ED3", width=40, height=10)
container_label.place(relx=0.5, rely=0.5, anchor="center")

# Create and place widgets inside the container
username_label = tk.Label(container_label, text="Username:", bg="#214ED3")
username_entry = tk.Entry(container_label)

password_label = tk.Label(container_label, text="Password:", bg="#214ED3")
password_entry = tk.Entry(container_label, show="*")

login_button = tk.Button(container_label, text="Login", command=login)

# Place the widgets inside the container
username_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
username_entry.grid(row=0, column=1, padx=10, pady=10)

password_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
password_entry.grid(row=1, column=1, padx=10, pady=10)

login_button.grid(row=2, column=1, pady=10)
# Run the Tkinter event loop
root.mainloop()

# Close the database connection
cursor.close()
db.close()
