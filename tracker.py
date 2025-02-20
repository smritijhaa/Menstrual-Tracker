import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime, timedelta
from tkinter import messagebox

class MenstrualTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Menstrual Tracker")
        self.root.geometry("600x600")
        self.root.configure(bg="#f9c8d3")  # Set background color to light pink

        # Initialize the list of past cycles to keep track of entered data
        self.past_cycles = []

        # Set up the calendar with highlighting of periods
        self.calendar = Calendar(self.root, selectmode="day", date_pattern="yyyy-mm-dd", font=("Arial", 12))
        self.calendar.pack(pady=20)  # Ensure the calendar is packed and visible

        # Input fields for start and end dates, and flow type
        self.create_input_fields()

        # Buttons for adding cycle, predicting next period, and viewing history
        self.create_buttons()

        # Label and text box to display cycle history and predictions
        self.create_history_and_prediction_widgets()

    def create_input_fields(self):
        """Create input fields for start date, end date, and flow type."""
        self.start_date_label = tk.Label(self.root, text="Start Date (YYYY-MM-DD):", font=("Arial", 12), bg="#f9c8d3", fg="#9c4d7d")
        self.start_date_label.pack(pady=5)

        self.start_date_entry = tk.Entry(self.root, font=("Arial", 12))
        self.start_date_entry.pack(pady=5)

        self.end_date_label = tk.Label(self.root, text="End Date (YYYY-MM-DD):", font=("Arial", 12), bg="#f9c8d3", fg="#9c4d7d")
        self.end_date_label.pack(pady=5)

        self.end_date_entry = tk.Entry(self.root, font=("Arial", 12))
        self.end_date_entry.pack(pady=5)

        self.flow_label = tk.Label(self.root, text="Flow (light, medium, heavy):", font=("Arial", 12), bg="#f9c8d3", fg="#9c4d7d")
        self.flow_label.pack(pady=5)

        self.flow_var = tk.StringVar()
        self.flow_var.set("light")
        self.flow_menu = tk.OptionMenu(self.root, self.flow_var, "light", "medium", "heavy")
        self.flow_menu.pack(pady=5)

    def create_buttons(self):
        """Create buttons for adding cycles, predicting next period, and viewing history."""
        self.add_button = tk.Button(self.root, text="Add Cycle", font=("Arial", 14), bg="#ff63a5", fg="white", command=self.add_cycle, relief="raised", borderwidth=2, highlightthickness=2, highlightbackground="#ff63a5", highlightcolor="#ff63a5", activebackground="#ff3881", activeforeground="white")
        self.add_button.pack(pady=10)

        self.predict_button = tk.Button(self.root, text="Predict Next Period", font=("Arial", 14), bg="#ff63a5", fg="white", command=self.predict_next_period, relief="raised", borderwidth=2, highlightthickness=2, highlightbackground="#ff63a5", highlightcolor="#ff63a5", activebackground="#ff3881", activeforeground="white")
        self.predict_button.pack(pady=10)

    def create_history_and_prediction_widgets(self):
        """Create widgets for showing cycle history and predictions."""
        self.prediction_label = tk.Label(self.root, text="", font=("Arial", 12), bg="#f9c8d3", fg="#9c4d7d")
        self.prediction_label.pack(pady=10)

    def add_cycle(self):
        """Handle adding a new cycle (start date, end date, and flow)."""
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        flow = self.flow_var.get()

        # Basic input validation to ensure dates are entered in the correct format
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter the date in the format YYYY-MM-DD.")
            return

        # Store the cycle in the list of past cycles for later use in predictions
        self.past_cycles.append({"start": start_date_obj, "end": end_date_obj, "flow": flow})

        # Highlight the cycle on the calendar
        self.highlight_calendar(start_date_obj, end_date_obj, flow)

        # Clear input fields for the next entry
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)

        messagebox.showinfo("Cycle Added", f"Cycle added. Start Date: {start_date}, End Date: {end_date}, Flow: {flow}")

    def highlight_calendar(self, start_date, end_date, flow):
        """Highlight the calendar with the start and end dates of the period."""
        current_date = start_date
        while current_date <= end_date:
            # Create an event on each date of the period, tagged by flow type
            self.calendar.calevent_create(current_date, 'Period', tags=flow)
            current_date += timedelta(days=1)

    def predict_next_period(self):
        """Predict the next period based on average cycle length from past cycles."""
        if len(self.past_cycles) < 2:  # Need at least two cycles to predict
            messagebox.showerror("Not Enough Data", "Please add at least two cycles to predict the next period.")
            return

        # Calculate the average cycle length (difference between consecutive cycles)
        cycle_lengths = []
        for i in range(1, len(self.past_cycles)):
            prev_cycle_end = self.past_cycles[i - 1]["end"]
            current_cycle_start = self.past_cycles[i]["start"]
            cycle_lengths.append((current_cycle_start - prev_cycle_end).days)

        avg_cycle_length = sum(cycle_lengths) / len(cycle_lengths)

        # Predict the next start date based on the average cycle length
        last_cycle_end = self.past_cycles[-1]["end"]
        next_period_start = last_cycle_end + timedelta(days=avg_cycle_length)

        # Display the predicted next period start date
        self.prediction_label.config(text=f"Predicted next period start date: {next_period_start.strftime('%Y-%m-%d')}")
