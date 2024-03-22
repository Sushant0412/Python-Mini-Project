import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import sys
import os

def open_home_with_action(action, username=None):
    if action == "home.py":
        subprocess.Popen(["python", action, username])
    elif action == "login.py":
        # Perform logout functionality or redirect to login page
        print("Logging out...")
        subprocess.Popen(["python", action])
    elif action == "add.py":
        subprocess.Popen(["python", action, username])
        # Perform Add Property functionality
        print("Opening Add Property page...")
    elif action == "delete.py":
        subprocess.Popen(["python", action, username])
        # Perform Delete Property functionality
        print("Opening Delete Property page...")
    elif action == "search.py":
        subprocess.Popen(["python", action, username])
        # Perform Search Property functionality
        print("Opening Search Property page...")

    os._exit(0)  # Terminate the current process

# Example usage:
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python landing.py <username>")
        sys.exit(1)

    username = sys.argv[1]

    # Create the main window
    window = tk.Tk()
    window.title("Real Estate App")
    #window.geometry("800x600")  # Set window size to 800x600 pixels

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 800
    window_height = 600
    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)

    # Set window size and position
    window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Load the image from desktop
    image_path = "./images/Landing.png"  # Update the path with your desktop username
    image = Image.open(image_path)
    image = image.resize((800, 600), Image.LANCZOS)  # Resize image to fit window

    # Convert Image object to Tkinter PhotoImage object
    photo = ImageTk.PhotoImage(image)

    # Create a label for the image
    image_label = tk.Label(window, image=photo)
    image_label.place(x=0, y=0, relwidth=1, relheight=1)  # Stretch the image to fill the window

    # Create buttons to open home.py with different actions
    add_button = tk.Button(window, text="Add Property", command=lambda: open_home_with_action("add.py", username))
    add_button.place(x=95, y=480)  # Adjust the coordinates as needed

    delete_button = tk.Button(window, text="Delete Property", command=lambda: open_home_with_action("delete.py", username))
    delete_button.place(x=435, y=480)  # Adjust the coordinates as needed

    search_button = tk.Button(window, text="Search Property", command=lambda: open_home_with_action("search.py", username))
    search_button.place(x=260, y=480)  # Adjust the coordinates as needed

    logout_button = tk.Button(window, text="Logout", command=lambda: open_home_with_action("login.py"))
    logout_button.place(x=630, y=480)  # Adjust the coordinates as needed


    # Start the main loop
    window.mainloop()

#9885011204