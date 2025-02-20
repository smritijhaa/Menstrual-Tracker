Menstrual Tracker Application
A simple, user-friendly menstrual cycle tracker built with Python's Tkinter GUI and JSON for user authentication. This app allows users to log their menstrual cycles, predict the next period, and view their cycle history.

Features

- User Authentication:
  Login and registration system to store user credentials in a users.json file.
  
-Track Menstrual Cycles:
  Add start and end dates for each cycle along with flow type (light, medium, heavy).
  Visual calendar integration to highlight cycle dates.
  
-Predict Next Period:
  Based on historical data, predict the next period start date.
  
-Cycle History:
  View the history of all logged menstrual cycles.

Requirements
- Python (version 3.x)
- Tkinter (for GUI development, comes pre-installed with Python)
- tkcalendar (for calendar widget)
  - You can install tkcalendar using pip if you don't have it installed already:
    pip install tkcalendar

Installation
- Clone or download the repository to your local machine.
- Navigate to the project folder.
- Install required libraries using pip (if you don't have them already):

How to Run the Application
- Open a terminal or command prompt.
- Navigate to the directory where main.py is located.
- Run the application by executing:
  python main.py
- The login page will appear first. If you have an existing account, you can log in. If not, you can register a new account.
- Once logged in, you will be taken to the menstrual tracker page where you can:
  Add your menstrual cycle details.
  Predict your next period start date.
  View your cycle history on the calendar.


Usage
Login/Registration:
- On the login page, enter your username and password.
- If you are a new user, click on "Register" (second button) to create an account.
- Menstrual Tracker:

After logging in, you will see a calendar and input fields for adding your cycle data.
Enter the start date, end date, and flow type (light, medium, heavy).
Click "Add Cycle" to add the cycle to the calendar.
The system will also show the prediction for your next period based on previous cycles (once two or more have been recorded.)
