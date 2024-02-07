import tkinter as tk

def button_clicked():
    label.config(text="Button Clicked!")

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
