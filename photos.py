import tkinter as tk
import sys

def button_clicked():
    global plot_id
    label.config(text="Hello, " + plot_id)

if len(sys.argv) > 1:
    plot_id = sys.argv[1]
else:
    plot_id = "No plot_id provided."

# Create the main window
root = tk.Tk()
root.title("Simple Tkinter Example")

# Create a label widget
label = tk.Label(root, text="Hello, Tkinter!")
label.pack(pady=20)

# Create a button widget
button = tk.Button(root, text="Click Me", command=button_clicked)
button.pack()

# Run the Tkinter event loop
root.mainloop()
