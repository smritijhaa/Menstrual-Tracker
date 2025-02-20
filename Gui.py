import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import datetime
import json

# Function to load users from the "users.json" file
def load_users():
    try:
        # Attempt to load the user data from a JSON file
        with open("users.json", "r") as file:
            return json.load(file)  # Return the loaded user data
    except FileNotFoundError:
        # If the file doesn't exist, return an empty dictionary
        return {}

# Function to save a new user (username and password) to the "users.json" file
def save_user(username, password):
    users = load_users()  # Load current users
    users[username] = password  # Add the new user
    with open("users.json", "w") as file:
        json.dump(users, file)  # Save the updated user data back to the file

class MenstrualTrackerApp:
    def __init__(self, root):
        """Initialize the main application window and set up UI elements."""
        self.root = root
        self.root.title("Menstrual Tracker")  # Set the title of the window
        self.root.geometry("600x600")  # Set the window size
        self.root.configure(bg="#f9c8d3")  # Set background color to light pink

        self.tracker = MenstrualTracker()  # Create an instance of MenstrualTracker to manage cycle data

        # Set up the calendar widget to allow date selection
        self.calendar = Calendar(self.root, selectmode="day", date_pattern="yyyy-mm-dd", font=("Arial", 12))
        self.calendar.pack(pady=20)

        # Create input fields for start date, end date, and flow type
        self.create_input_fields()

        # Create buttons for adding cycles, predicting next period, and viewing cycle history
        self.create_buttons()

        # Create widgets to display cycle history and prediction results
        self.create_history_and_prediction_widgets()

    def create_input_fields(self):
        """Create input fields for start date, end date, and flow type."""
        # Label and input field for Start Date
        self.start_date_label = tk.Label(self.root, text="Start Date (YYYY-MM-DD):", font=("Arial", 12), bg="#f9c8d3", fg="#9c4d7d")
        self.start_date_label.pack(pady=5)

        # Label and input field for End Date
        self.end_date_label = tk.Label(self.root, text="End Date (YYYY-MM-DD):", font=("Arial", 12), bg="#f9c8d3", fg="#9c4d7d")
        self.end_date_label.pack(pady=5)

        self.start_date_entry = tk.Entry(self.root, font=("Arial", 12))  # Entry field for start date
        self.start_date_entry.pack(pady=5)

        self.end_date_entry = tk.Entry(self.root, font=("Arial", 12))  # Entry field for end date
        self.end_date_entry.pack(pady=5)

        # Label and dropdown for Flow type (light, medium, heavy)
        self.flow_label = tk.Label(self.root, text="Flow (light, medium, heavy):", font=("Arial", 12), bg="#f9c8d3", fg="#9c4d7d")
        self.flow_label.pack(pady=5)

        self.flow_var = tk.StringVar()  # Variable to store the selected flow type
        self.flow_var.set("light")  # Default value for flow type
        self.flow_menu = tk.OptionMenu(self.root, self.flow_var, "light", "medium", "heavy")  # Dropdown menu for flow options
        self.flow_menu.pack(pady=5)

    def create_buttons(self):
        """Create the buttons for adding cycles, predicting next period, and viewing cycle history."""
        # Button to add a new cycle
        self.add_button = tk.Button(self.root, text="Add Cycle", font=("Arial", 14), bg="#ff63a5", fg="white",
                                    command=self.add_cycle, relief="raised", borderwidth=2, highlightthickness=2,
                                    highlightbackground="#ff63a5", highlightcolor="#ff63a5",
                                    activebackground="#ff3881", activeforeground="white")
        self.add_button.pack(pady=10)

        # Button to predict the next cycle based on average cycle length
        self.predict_button = tk.Button(self.root, text="Predict Next Period", font=("Arial", 14), bg="#ff63a5",
                                        fg="white", command=self.predict_next_period, relief="raised", borderwidth=2,
                                        highlightthickness=2, highlightbackground="#ff63a5", highlightcolor="#ff63a5",
                                        activebackground="#ff3881", activeforeground="white")
        self.predict_button.pack(pady=10)

        # Force the background color to be consistent when the window is focused or switched
        self.root.bind("<FocusIn>", self.ensure_button_colors)

    def ensure_button_colors(self, event=None):
        """Ensure the button colors remain consistent when the window is focused or switched."""
        # Reset the button colors when the window is focused or switched
        self.add_button.config(bg="#ff63a5", activebackground="#ff3881", fg="white")
        self.predict_button.config(bg="#ff63a5", activebackground="#ff3881", fg="white")

    def create_history_and_prediction_widgets(self):
        """Create widgets for showing cycle history and predictions."""
        # Label to show prediction for the next cycle start date
        self.prediction_label = tk.Label(self.root, text="", font=("Arial", 12), bg="#f9c8d3", fg="#9c4d7d")
        self.prediction_label.pack(pady=10)

        # Text box to display the cycle history (previous cycles)
        self.history_text = tk.Text(self.root, height=5, width=40, font=("Arial", 12), bg="#f9c8d3", fg="#9c4d7d", bd=2,
                                    wrap="word")
        self.history_text.pack(pady=10)

    def add_cycle(self):
        """Handle adding a new cycle."""
        # Get the start and end date inputs, as well as the flow type selected
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        flow = self.flow_var.get()

        # Basic input validation to ensure the dates are in the correct format
        try:
            datetime.datetime.strptime(start_date, "%Y-%m-%d")
            datetime.datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter the date in the format YYYY-MM-DD.")  # Show error if dates are invalid
            return

        self.tracker.add_cycle(start_date, end_date, flow)  # Add the cycle data to the tracker
        messagebox.showinfo("Cycle Added", f"Cycle added. Start Date: {start_date}, End Date: {end_date}, Flow: {flow}")

        # Highlight the start and end date on the calendar
        self.highlight_calendar(start_date, end_date, flow)

        # Clear the input fields after adding the cycle
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)

    def highlight_calendar(self, start_date, end_date, flow):
        """Highlight the calendar with the start and end dates of the period."""
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        # Loop through the dates and mark them as part of the period on the calendar
        current_date = start
        while current_date <= end:
            self.calendar.calevent_create(current_date, 'Period', tags=flow)  # Mark each day as part of the period
            current_date += datetime.timedelta(days=1)

    def predict_next_period(self):
        """Predict the next period based on average cycle length."""
        next_period = self.tracker.predict_next_period()  # Get the predicted start date for the next period
        if next_period:
            self.prediction_label.config(text=f"Predicted next period start date: {next_period}")  # Show the predicted date
        else:
            self.prediction_label.config(text="Not enough data to predict next period.")  # Show message if there isn't enough data

class LoginPage:
    def __init__(self, root):
        """Initialize the login page."""
        self.root = root
        self.root.title("Login")  # Set the title of the login window
        self.root.geometry("400x300")  # Set the login window size
        self.root.configure(bg="#f9c8d3")  # Set background color to light pink

        # Create the login interface
        self.username_label = tk.Label(self.root, text="Username:", font=("Arial", 12), bg="#f9c8d3", fg="#9c4d7d")
        self.username_label.pack(pady=5)

        self.username_entry = tk.Entry(self.root, font=("Arial", 12))  # Input field for username
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.root, text="Password:", font=("Arial", 12), bg="#f9c8d3", fg="#9c4d7d")
        self.password_label.pack(pady=5)

        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 12))  # Input field for password (with masking)
        self.password_entry.pack(pady=5)

        # Button to attempt login
        self.login_button = tk.Button(self.root, text="Login", font=("Arial", 14), bg="#ff63a5", fg="white", command=self.login)
        self.login_button.pack(pady=10)

        # Button to open registration page
        self.register_button = tk.Button(self.root, text="Register", font=("Arial", 14), bg="#ff63a5", fg="white", command=self.register)
        self.register_button.pack(pady=10)

    def login(self):
        """Handle login by checking if the username and password are correct."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Load the users from the "users.json" file
        users = load_users()
        if username in users and users[username] == password:
            messagebox.showinfo("Login Successful", "Welcome to the Menstrual Tracker!")  # Success message
            self.root.destroy()  # Close the login window
            self.show_tracker_page()  # Open the menstrual tracker page
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")  # Error message if login fails

    def register(self):
        """Handle registration by adding a new user."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Save the new user to the "users.json" file
        save_user(username, password)
        messagebox.showinfo("Registration Successful", "You have successfully registered.")  # Success message
