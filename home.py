import tkinter as tk
from tkinter import messagebox
import login

class HomePage:
    def __init__(self, master):
        self.master = master
        master.title("Home Page")

        # Add your home page components
        home_label = tk.Label(master, text="Welcome to the Home Page!")
        home_label.pack()

        # Navigation Bar
        navbar_frame = tk.Frame(master)
        navbar_frame.pack(pady=50, padx=50)

        logout_button = tk.Button(navbar_frame, text="Logout", command=self.logout)
        logout_button.pack(side=tk.RIGHT)

    def logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            self.master.destroy()  # Close the home window and return to the login window
            # self.master.quit()
            login.open_login_page()

def open_home_page():
    home_window = tk.Tk()
    home_page = HomePage(home_window)
    home_window.mainloop()

# Example usage
if __name__ == "__main__":
    open_home_page()
