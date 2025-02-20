import tkinter as tk
from tkinter import messagebox
import json
from tracker import MenstrualTrackerApp  # Importing the Menstrual Tracker app page

# Function to load the users from the JSON file
def load_users():
    try:
        # Try to open the "users.json" file and load the data
        with open("users.json", "r") as file:
            return json.load(file)  # Return the data (users) in JSON format
    except FileNotFoundError:
        # If the file doesn't exist, return an empty dictionary
        return {}

# Function to save a new user to the "users.json" file
def save_user(username, password):
    users = load_users()  # Load the current users
    users[username] = password  # Add the new user with their password
    with open("users.json", "w") as file:
        json.dump(users, file)  # Save the updated users data to the file

# Class to handle the login page interface
class LoginPage:
    def __init__(self, root):
        self.root = root  # Reference to the main window (root)
        self.root.title("Login")  # Set the window title
        self.root.geometry("400x300")  # Set the window size (width x height)
        self.root.configure(bg="#f9c8d3")  # Set the background color to light pink

        # Create the "Username" label
        self.username_label = tk.Label(self.root, text="Username:", font=("Arial", 12), bg="#f9c8d3", fg="#9c4d7d")
        self.username_label.pack(pady=5)  # Add the label to the window with padding

        # Create the username input field (Entry widget)
        self.username_entry = tk.Entry(self.root, font=("Arial", 12))
        self.username_entry.pack(pady=5)  # Add the entry field with padding

        # Create the "Password" label
        self.password_label = tk.Label(self.root, text="Password:", font=("Arial", 12), bg="#f9c8d3", fg="#9c4d7d")
        self.password_label.pack(pady=5)  # Add the label to the window with padding

        # Create the password input field (Entry widget) and set it to hide text input
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=5)  # Add the entry field with padding

        # Create the "Login" button that calls the login method when clicked
        self.login_button = tk.Button(self.root, text="Login", font=("Arial", 14), bg="#ff63a5", fg="white", command=self.login)
        self.login_button.pack(pady=10)  # Add the button to the window with padding

        # Create the "Register" button that calls the register method when clicked
        self.register_button = tk.Button(self.root, text="Register", font=("Arial", 14), bg="#ff63a5", fg="white", command=self.register)
        self.register_button.pack(pady=10)  # Add the button to the window with padding

    def login(self):
        """Handles the login process by verifying the username and password."""
        username = self.username_entry.get()  # Get the entered username
        password = self.password_entry.get()  # Get the entered password

        users = load_users()  # Load the saved users from the JSON file
        if username in users and users[username] == password:
            # If the username exists and the password matches
            messagebox.showinfo("Login Successful", "Welcome to the Menstrual Tracker!")  # Show success message
            self.root.destroy()  # Close the login window
            self.show_tracker_page()  # Open the Menstrual Tracker page
        else:
            # If the login fails (wrong username or password)
            messagebox.showerror("Login Failed", "Invalid username or password.")  # Show error message

    def register(self):
        """Handles the registration process by saving a new user."""
        username = self.username_entry.get()  # Get the entered username
        password = self.password_entry.get()  # Get the entered password

        if username and password:
            # If both the username and password are provided
            save_user(username, password)  # Save the new user to the JSON file
            messagebox.showinfo("Registration Successful", "You can now log in with your credentials.")  # Show success message
        else:
            # If either username or password is missing
            messagebox.showerror("Registration Failed", "Please enter both a username and password.")  # Show error message

    def show_tracker_page(self):
        """Opens the Menstrual Tracker page after a successful login."""
        tracker_root = tk.Tk()  # Create a new window for the Menstrual Tracker page
        tracker_root.title("Menstrual Tracker")  # Set the title for the tracker page
        menstrual_app = MenstrualTrackerApp(tracker_root)  # Create an instance of the MenstrualTrackerApp class
        tracker_root.mainloop()  # Start the tkinter event loop for the tracker page

