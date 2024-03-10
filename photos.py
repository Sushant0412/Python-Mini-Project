import tkinter as tk
import sys
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

def add_rating(plot_id, rating, username):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='project',
            user='root',
            password='test'
        )
        if connection.is_connected():
            cursor = connection.cursor()

            # Check if plot_id already exists for the current owner
            cursor.execute("SELECT rating FROM ratings WHERE plot_id = %s AND owner = %s", (plot_id, username))
            existing_rating = cursor.fetchone()

            if existing_rating is None:
                # If plot_id doesn't exist for the current owner, insert the new rating
                sql_query = "INSERT INTO ratings (plot_id, rating, owner) VALUES (%s, %s, %s)"
                cursor.execute(sql_query, (plot_id, rating, username))
            else:
                # If plot_id exists for the current owner, calculate the average rating
                existing_rating = existing_rating[0]
                new_rating = (existing_rating + rating) / 2.0
                # Update the rating in the database
                sql_query = "UPDATE ratings SET rating = %s WHERE plot_id = %s AND owner = %s"
                cursor.execute(sql_query, (new_rating, plot_id, username))

            # Commit the transaction
            connection.commit()
            messagebox.showinfo("Success", "Rating added/updated successfully.")
    except Error as e:
        print("Error:", e)
        messagebox.showerror("MySQL Error", f"Error: {e.msg}")
    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()

def button_clicked(entry, plot_id, username):
    rating = entry.get()
    try:
        rating = float(rating)
        if 0 <= rating <= 5:
            add_rating(plot_id, rating, username)
        else:
            print("Invalid rating. Please enter a rating between 0 and 5.")
            messagebox.showerror("Invalid Rating", "Please enter a rating between 0 and 5.")
    except ValueError:
        print("Invalid rating. Please enter a number.")
        messagebox.showerror("Invalid Rating", "Please enter a number for the rating.")

def main():
    if len(sys.argv) > 2:
        plot_id = sys.argv[1]
        username = sys.argv[2]
        print(f"Welcome, {username}!")
    else:
        print("No plot_id or username provided.")
        sys.exit(1)  # Exit the script if no plot_id or username is provided

    root = tk.Tk()
    root.title("Rating Page")
    root.geometry("400x200")

    # Create a Label widget for rating input
    label = tk.Label(root, text="Enter Rating (0-5):")
    label.pack(pady=10)

    # Create an Entry widget for rating input
    entry = tk.Entry(root)
    entry.pack()

    # Create a Button widget to submit rating
    button = tk.Button(root, text="Submit Rating", command=lambda: button_clicked(entry, plot_id, username))
    button.pack(pady=10)

    # Run the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
