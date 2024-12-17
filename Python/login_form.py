# ----------------------------------------------------
# Team041
# Sailesh Arya, Brian Jiang, Aaron Job Ramirez, Nick vanVeldhuisen
# Class purpose: Login form
# Depends On: TK for forms, nwauto.py for MySQL functions
# ----------------------------------------------------

import nwauto
import tkinter as tk
from tkinter import font

class LoginForm:
        def __init__(self, master, parent_form):
                self.root = master
                self.root.protocol("WM_DELETE_WINDOW", self.cancel)
                master.geometry("350x100")
                # color = master.winfo_rgb('red'), 
                self.parent_form = parent_form
                master.title("Login Form")
                self.username_label = tk.Label(self.root, text="User Name:")
                self.username_label.grid(row=0, column=0)
                self.usernamevar = tk.StringVar() #creates StringVar to store contents of entry
                self.username_entry = tk.Entry(self.root, textvariable = self.usernamevar)
                self.username_entry.focus_set() # PUT CURSOR HERE!
                self.username_entry.grid(row=0, column=1, sticky='w')
                self.username_entry.config({"background": "pink"}) # Input required
                
                # Create and place the password label and entry
                self.password_label = tk.Label(self.root, text="Password:")
                self.password_label.grid(row=1, column=0)
                self.passwordvar = tk.StringVar() #creates StringVar to store contents of entry
                self.password_entry = tk.Entry(self.root, show="*", textvariable = self.passwordvar)  # Show asterisks for password
                self.password_entry.grid(row=1, column=1, sticky='w')
                self.password_entry.bind("<Return>", self.validate_login_caller)
                self.password_entry.config({"background": "pink"}) # Input required

                # Create and place the login button
                self.login_button = tk.Button(self.root, text="Login", command=self.validate_login)
                self.login_button.grid(row=2, column=0, sticky='w') # Create and place the login button
                self.login_button.config(state="disabled")
                self.cancel_button = tk.Button(self.root, text="Cancel", command=self.cancel)
                self.cancel_button.grid(row=2, column=1, sticky='w') # Create and place the Cancel button
                self.errorfont = font.Font(family="Arial", size=12, weight="bold") # Match vehicle search
                self.login_error = tk.Label(self.root, text="Input Required. Case Sensitive", anchor="e", fg="red", font=self.errorfont)
                self.login_error.grid(row=3, column=0, columnspan=3, sticky='w') # Error message

                # Have to put these here because of calls to input_required before UI objects defined
                self.passwordvar.trace_add(mode=['read','write'], callback=self.input_required)
                self.usernamevar.trace_add(mode=['read','write'], callback=self.input_required)

        # I am sure there is a more clever way to do this
        def input_required(self, *args):
                if len(self.usernamevar.get()) > 0 and  len(self.passwordvar.get()) > 0 :
                        self.login_button.config(state="normal")
                        #self.login_error.config(text="Click submit to login.")
                else:
                        self.login_button.config(state="disabled")
                        self.login_error.config(text="Input Required. Case Sensitive.")
                if len(self.usernamevar.get()) > 0:
                        self.username_entry.config({"background": "White"}) # Input received
                else:
                        self.username_entry.config({"background": "pink"}) # Input required
                if len(self.passwordvar.get()) > 0:
                        self.password_entry.config({"background": "White"}) # Input received
                else:
                        self.password_entry.config({"background": "pink"}) # Input required

        # Function to close the login form
        def cancel(self):
                print("Cancel")
                self.root.destroy()
                self.root.update()
                    
        # Function to validate the login
        def login(username, password):
                if nwauto.login(username, password):
                    print("Successful login")
                else:
                    print("Failed login")

        # ----------------------------------------------------
        # CR wrapper
        # ----------------------------------------------------
        def validate_login_caller(self, event):
                self.validate_login()

        # Function to pass the login input from the login form to the login function
        def validate_login(self):
            username = self.username_entry.get()
            password = self.password_entry.get()
 
            # You can add your own validation logic here
            if nwauto.login(username, password):
                self.login_error.config(text="Successful!")
                self.parent_form.show_privileged_interface() # Show interface elements relevant to "Privileged user" including search table/results
                self.parent_form.position_label["text"] = "USER: " + nwauto.get_username() # Show who is logged in
                # Close the login form
                self.root.destroy()
                self.root.update()
            else:
                self.login_error.config(text="Invalid username or password.")




