import tkinter as tk
from tkinter import messagebox
import mysql.connector
import home
from PIL import Image, ImageTk
import os

class LoginPage:
    @classmethod
    def create_login_page(cls):
        root = tk.Tk()
        login_page = cls(root)
        root.mainloop()
        
    def __init__(self, master):
        self.master = master
        master.title("Login Form")

        # Set window size and position
        window_width = 800
        window_height = 600
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        master.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Add background image
        bg_image_path = "./images/introImage.jpg"
        self.add_background_image(bg_image_path)

        # Create a frame for content
        content_frame = tk.Frame(master, bg="white", bd=50)
        content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6)

        # Create and place the username label and entry
        self.username_label = tk.Label(content_frame, text="Userid:", width=10)
        self.username_label.pack(pady=10)  # Add vertical padding

        self.username_entry = tk.Entry(content_frame, width=30)
        self.username_entry.pack(pady=10)

        # Create and place the password label and entry
        self.password_label = tk.Label(content_frame, text="Password:", width=10)
        self.password_label.pack(pady=10)

        self.password_entry = tk.Entry(content_frame, show="*", width=30)
        self.password_entry.pack(pady=10)

        # Create and place the login button
        self.login_button = tk.Button(content_frame, text="Login", command=self.check_credentials)
        self.login_button.pack(pady=10)

        # Database connection
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="test",
            database="project"
        )

        master.protocol("WM_DELETE_WINDOW", self.handle_close)

    def add_background_image(self, path):
        abs_path = os.path.abspath(path)
        
        # Open image with Pillow
        pil_image = Image.open(abs_path)

        # Convert the Pillow image to a format compatible with PhotoImage
        tk_image = ImageTk.PhotoImage(pil_image)

        # Create a label with the image
        background_label = tk.Label(self.master, image=tk_image)
        background_label.image = tk_image  # Keep a reference to avoid garbage collection
        background_label.place(relwidth=1, relheight=1)

    def check_credentials(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            cursor = self.db.cursor()

            # Query to check credentials in the database
            query = "SELECT * FROM login WHERE user=%s AND pass=%s"
            cursor.execute(query, (username, password))
            
            result = cursor.fetchone()

            if result:
                self.master.withdraw()  # Hide the login window
                home.open_home_page()   # Open the home window
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")

            cursor.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def handle_close(self):
        # This method is called when the user clicks the close button (X)
        confirm = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if confirm:
            self.master.destroy()  # Close the login window
            # Optionally, you might want to add code to clean up resources or perform additional actions before exiting
    
# Create the main window
def open_login_page():
    login_window = tk.Tk()
    login_page = LoginPage(login_window)
    login_window.mainloop()

# Start the Tkinter event loop
if __name__ == "__main__":
    open_login_page()
