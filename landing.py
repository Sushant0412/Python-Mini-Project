import tkinter as tk
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
    elif action == "home.py":
        # Perform Delete Property functionality
        print("Opening Delete Property page...")
    elif action == "home.py":
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
    window.geometry("800x600")  # Set window size to 800x600 pixels

    # Create a label with the real estate quote
    quote_label = tk.Label(window, text="Real estate quote goes here", font=("Arial", 14))
    quote_label.pack(pady=20)

    # Create buttons to open home.py with different actions
    add_button = tk.Button(window, text="Add Property", command=lambda: open_home_with_action("add.py", username))
    add_button.pack()

    delete_button = tk.Button(window, text="Delete Property", command=lambda: open_home_with_action("home.py", username))
    delete_button.pack()

    search_button = tk.Button(window, text="Search Property", command=lambda: open_home_with_action("home.py", username))
    search_button.pack()

    logout_button = tk.Button(window, text="Logout", command=lambda: open_home_with_action("login.py"))
    logout_button.pack()

    # Start the main loop
    window.mainloop()
