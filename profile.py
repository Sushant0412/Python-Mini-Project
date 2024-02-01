import tkinter as tk
from tkinter import messagebox
import subprocess

def back():
    subprocess.Popen(["python", "home.py"])  # Replace "python" with your Python interpreter if needed
    root.destroy()

root = tk.Tk()
root.title("Profile Page")

# Your profile page content goes here

back_button = tk.Button(root, text="Back", command=back)
back_button.pack()

# Run the Tkinter event loop
root.mainloop()
