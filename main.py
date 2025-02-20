import tkinter as tk
from login import LoginPage  # Import the LoginPage class from the login.py file

# The main function where the program starts
def main():
    root = tk.Tk()  # Create the main window (root) for the application
    login_page = LoginPage(root)  # Create an instance of the LoginPage class and pass the root window to it
    root.mainloop()  # Start the tkinter event loop to display the login page and handle user interactions

# This checks if this file is being run directly (not imported as a module)
if __name__ == "__main__":
    main()  # Call the main function to start the program
