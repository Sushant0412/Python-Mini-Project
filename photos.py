import tkinter as tk
import sys
import mysql.connector
from mysql.connector import Error

def add_rating(plot_id, rating):
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
            print("Rating added/updated successfully.")
    except Error as e:
        print("Error:", e)
    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()



def button_clicked():
    global plot_id
    label.config(text="Hello, " + plot_id)
    rating = float(entry.get())
    if 0 <= rating <= 5:
        add_rating(plot_id, rating)
    else:
        print("Invalid rating. Please enter a rating between 0 and 5.")

if len(sys.argv) > 1:
    plot_id = sys.argv[1]
    username = sys.argv[2]
else:
    plot_id = "No plot_id provided."
    username = "No username provided."

# Create the main window
root = tk.Tk()
root.title("Simple Tkinter Example")

# Create a label widget
label = tk.Label(root, text="Hello, Tkinter!")
label.pack(pady=20)

# Create an Entry widget for rating input
entry = tk.Entry(root)
entry.pack()

# Create a button widget
button = tk.Button(root, text="Click Me", command=button_clicked)
button.pack()

# Run the Tkinter event loop
root.mainloop()