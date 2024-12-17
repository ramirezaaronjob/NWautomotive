# ----------------------------------------------------
# Team041
# Sailesh Arya, Brian Jiang, Aaron Job Ramirez, Nick vanVeldhuisen
# Python Class buy_vehicle.BuylVehicleForm
# Class purpose: Add New Vehicle Form
# Depends On: tkinger tk/tkk for forms
#             nwauto.py for MySQL database functions, session variables, etc.
#             add_customer.py and search_customer.py for add/search customer forms for customer id
# Called By: vehicle_search.py Vehicle Info button
# ----------------------------------------------------

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import nwauto
from add_customer import AddCustomerForm
from search_customer import SearchCustomerForm
import re
#import time

class BuyVehicleForm:
    def __init__(self, master, vin, parent_form):
        self.root = master
        self.root.protocol("WM_DELETE_WINDOW", self.cancel_form)
        self.parent_form = parent_form
        self.customer_id = -1
        self.stored_vin = None
        self.root.title("Buy Vehicle Form")
        self.vin = tk.StringVar(value=vin)
        # Error message display
        self.error_label = tk.Label(master, text=f"Enter Vin and Customer", font=("Helvetica", 10, "normal"))
        self.setup_vin_section()
        self.setup_customer_section()
        self.populate_lookups()

    def showwarning(self,warning):
        self.error_label["text"]=warning

    def setup_vin_section(self):
        self.vin_label = tk.Label(self.root, text="VIN:", font=("Helvetica", 14, "bold"))
        self.vin_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.vin_entry = tk.Entry(self.root, textvariable=self.vin, bg="pink")
        self.vin_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.vin_entry.bind("<KeyRelease>", self.update_vin_background)
        self.check_vin_button = tk.Button(self.root, text="Check VIN", command=self.check_vin)
        self.check_vin_button.grid(row=0, column=2, padx=5, pady=5)

    def setup_customer_section(self):
        self.customer_label = tk.Label(self.root, text="Search/Add Customer", font=("Helvetica", 14, "bold"))
        self.customer_label.grid(row=1, columnspan=4, column=0, padx=10, pady=10)
        self.search_customer_button = tk.Button(self.root, text="Search Customer", command=self.search_customer, state="disabled")
        self.search_customer_button.grid(row=2, column=0, padx=5, pady=5)
        self.add_customer_button = tk.Button(self.root, text="Add Customer", command=self.add_customer, state="disabled")
        self.add_customer_button.grid(row=2, column=1, padx=5, pady=5)
        self.buy_vehicle_button = tk.Button(self.root, text="Buy Vehicle", state="disabled", command=self.open_add_vehicle_form)
        self.buy_vehicle_button.grid(row=2, column=2, padx=5, pady=5)
        self.cancel_button = tk.Button(self.root, text="Cancel", command=self.cancel_form)
        self.cancel_button.grid(row=2, column=3, padx=5, pady=5)
        self.error_label.grid(row=3, column=0, columnspan=4, pady=5, sticky="w")

    def cancel_form(self):
        self.parent_form.refresh_search() # Update parent form search because parts may be installed or vehicle may be sold!!!
        self.root.destroy()
        self.root.update()

    def update_vin_background(self, event):
        var = self.vin_entry.get().strip()
        if len(var) > 50:  
            var = self.vin_entry.get()
            self.vin_entry.delete(0, tk.END)  # Clear existing text
            self.vin_entry.insert(0,var[:50]) # Restrict to 50
        if len(var) > 0:
            self.vin_entry.config(bg="white")
            self.check_vin_button.config(state="normal")
        else:
            self.vin_entry.config(bg="pink")
            self.check_vin_button.config(state="disabled")

    def check_vin(self):
        vin = self.vin.get()
        records, columns = nwauto.get_query_results_with_columns("find_vehicle", {"vin": vin})

        if records:  
            self.showwarning("Vehicle already exists in the database.")
            self.disable_buttons()
        else:
            self.showwarning("Vehicle not in inventory. Select Customer.")
            self.stored_vin = vin  # Store the VIN after validation
            self.vin_entry.config(state="disabled")  # Disable entry to prevent changes
            self.check_vin_button.config(state="disabled")  # Disable the check button
            self.enable_buttons()

    def disable_buttons(self):
        self.search_customer_button.config(state="disabled")
        self.add_customer_button.config(state="disabled")
        self.buy_vehicle_button.config(state="disabled")

    def enable_buttons(self):
        self.search_customer_button.config(state="normal")
        self.add_customer_button.config(state="normal")

    def set_customer(self, customer_id, customer_name):
        self.customer_id = customer_id
        self.customer_label["text"] = f"Selected Customer: {customer_name}"
        self.buy_vehicle_button.config(state="normal")

    def search_customer(self):
        self.search_window = tk.Toplevel(self.root)
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        self.search_window.geometry("+%d+%d" %(x+10,y+10))
        self.search_window.transient(self.root)
        self.search_window.grab_set()
        SearchCustomerForm(self.search_window, self)

    def add_customer(self):
        self.add_window = tk.Toplevel(self.root)
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        self.add_window.geometry("+%d+%d" %(x+10,y+10))
        self.add_window.transient(self.root)
        self.add_window.grab_set()
        AddCustomerForm(self.add_window, self)

    def populate_lookups(self): # ADD LOCKS?
        self.manufacturer_options = ["Select"] + [str(item[0]) for item in nwauto.get_query_results("manufacturers", {})]
        self.vehicle_type_options = ["Select"] + [str(item[0]) for item in nwauto.get_query_results("vehicle_type", {})]
        self.fuel_type_options = ["Select"] + [str(item[0]) for item in nwauto.get_query_results("fuel_type", {})]
        self.condition_options = ["Select"] + [str(item[0]) for item in nwauto.get_query_results("conditions", {})]
        self.color_options = [str(item[0]) for item in nwauto.get_query_results("colors", {})] 

    def open_add_vehicle_form(self):
        self.add_vehicle_window = tk.Toplevel(self.root)
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        self.add_vehicle_window.geometry("+%d+%d" %(x+10,y+10))
        self.add_vehicle_window.title("Add Vehicle Details")
        tk.Label(self.add_vehicle_window, text="VIN:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.add_vehicle_window, text=self.stored_vin, font=("Helvetica", 12, "bold")).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Label(self.add_vehicle_window, text="Purchaser (Username):", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.add_vehicle_window, text=nwauto.get_username(), font=("Helvetica", 12, "bold")).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        tk.Label(self.add_vehicle_window, text="Seller (Customer ID):", font=("Helvetica", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.add_vehicle_window, text=self.customer_id, font=("Helvetica", 12, "bold")).grid(row=2, column=1, padx=5, pady=5, sticky="w")
        # Vehicle input fields
        self.vehicle_type = tk.StringVar()
        self.vehicle_type.set( "Select" )
        self.manufacturer = tk.StringVar()
        self.manufacturer.set( "Select" )
        self.model = tk.StringVar()
        self.model_year = tk.StringVar()
        self.fuel_type = tk.StringVar()
        self.fuel_type.set( "Select" )
        self.horsepower = tk.StringVar()
        self.condition = tk.StringVar()
        self.condition.set( "Select" )
        self.purchase_date = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        self.purchase_price = tk.StringVar()
        self.description = tk.StringVar()
        self.create_dropdown(self.add_vehicle_window, "Vehicle Type:", self.vehicle_type, self.vehicle_type_options, row=3)
        self.create_dropdown(self.add_vehicle_window, "Manufacturer:", self.manufacturer, self.manufacturer_options, row=4)
        self.model_entry = self.create_text_field(self.add_vehicle_window, "Model:", self.model, row=5)
        self.model_year_entry = self.create_text_field(self.add_vehicle_window, "Model Year:", self.model_year, row=6)
        self.create_dropdown(self.add_vehicle_window, "Fuel Type:", self.fuel_type, self.fuel_type_options, row=7)
        self.hp_entry = self.create_text_field(self.add_vehicle_window, "Horsepower:", self.horsepower, row=8)
        self.create_dropdown(self.add_vehicle_window, "Condition:", self.condition, self.condition_options, row=9)
        tk.Label(self.add_vehicle_window, text="Purchase Date", font=("Helvetica", 12)).grid(row=10, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.add_vehicle_window, text=self.purchase_date.get(), font=("Helvetica", 12)).grid(row=10, column=1, padx=5, pady=5, sticky="w")
        #self.create_text_field(self.add_vehicle_window, "Purchase Date:", self.purchase_date, row=10)
        self.price_entry = self.create_text_field(self.add_vehicle_window, "Purchase Price:", self.purchase_price, row=11)
        self.desc_entry = self.create_text_field(self.add_vehicle_window, "Description:", self.description, row=12)
        self.desc_entry.config({"background": "White"}) 

        tk.Label(self.add_vehicle_window, text="Colors:", font=("Helvetica", 12)).grid(row=13, column=0, padx=5, pady=5, sticky="w")
        self.color_listbox = tk.Listbox(self.add_vehicle_window, selectmode=tk.MULTIPLE, exportselection=0)
        for color in self.color_options:
            self.color_listbox.insert(tk.END, color)
        self.color_listbox .bind('<<ListboxSelect>>', self.input_required)
        self.color_listbox.grid(row=13, column=1, padx=5, pady=5, sticky="w")
        self.buy_error_label = tk.Label(self.add_vehicle_window, text=f"Enter Required Inputs", font=("Helvetica", 10, "normal"))
        self.buy_error_label.grid(row=14, column=0, columnspan=2, pady=5, sticky="w")
        self.submit_button = tk.Button(self.add_vehicle_window, text="Submit", command=self.submit_form, state=tk.DISABLED)
        self.submit_button.grid(row=15, column=1, pady=5, sticky="e")
        self.model.trace_add(mode=['write'], callback=self.input_required)
        self.model_year.trace_add(mode=['write'], callback=self.input_required)
        self.horsepower.trace_add(mode=['write'], callback=self.input_required)
        self.purchase_price.trace_add(mode=['write'], callback=self.input_required)
        self.description.trace_add(mode=['write'], callback=self.input_required)
        self.vehicle_type.trace_add(mode=['write'], callback=self.input_required)
        self.manufacturer.trace_add(mode=['write'], callback=self.input_required)
        self.fuel_type.trace_add(mode=['write'], callback=self.input_required)
        self.condition.trace_add(mode=['write'], callback=self.input_required)

    def showbuywarning(self,warning):
        self.buy_error_label["text"]=warning

    def create_dropdown(self, parent, label_text, variable, options, row):
        tk.Label(parent, text=label_text, font=("Helvetica", 12)).grid(row=row, column=0, padx=5, pady=5, sticky="w")
        dropdown = tk.OptionMenu(parent, variable, *options)
        dropdown.grid(row=row, column=1, padx=5, pady=5, sticky="w")

    def create_text_field(self, parent, label_text, variable, row):
        tk.Label(parent, text=label_text, font=("Helvetica", 12)).grid(row=row, column=0, padx=5, pady=5, sticky="w")
        entry = tk.Entry(parent, textvariable=variable)
        entry.grid(row=row, column=1, padx=5, pady=5, sticky="w")
        entry.config({"background": "pink"}) # Input required
        return entry

    def submit_form(self):
        current_year = datetime.now().year
        try:
            model_year = int(self.model_year.get())
            if model_year > current_year + 1:
                self.model_year_entry.config({"background": "pink"})
                return
            else:
                self.model_year_entry.config({"background": "white"})
        except ValueError:
            self.model_year_entry.config({"background": "pink"})
            return
            
        var_dict = {
            "vin": self.stored_vin,
            "purchaser": nwauto.get_username(),
            "seller": str(self.customer_id),
            "vehicle_type": self.vehicle_type.get(),
            "manufacturer": self.manufacturer.get(),
            "model": self.model.get(),
            "year": self.model_year.get(),
            "fuel_type": self.fuel_type.get(),
            "horsepower": self.horsepower.get(),
            "condition": self.condition.get(),
            "purchase_date": self.purchase_date.get(),
            "purchase_price": self.purchase_price.get(),
            "description": self.description.get()
        }
        # Check data received
        if any(value == "" or value == "Select" for key, value in var_dict.items() if key != "description"):
            self.showbuywarning("Please fill out all required fields.")
            return
        # Check data typing
        if not (var_dict["horsepower"].isdigit() and len(var_dict["horsepower"]) < 5):
            self.showbuywarning("Horsepower must be an integer with no more than 4 digits.")
            return
        if not (self.is_float_convertible(var_dict["purchase_price"])):
            self.showbuywarning("Price must be an number.")
            return
        try:
            nwauto.run_lock("buy_vehicle_locks")
            if nwauto.run_dml("buy_vehicle", var_dict) < 0:
                self.showbuywarning("Error buying vehicle. Check input or contact support.")
                nwauto.run_unlock()
                return
            selected_colors = [self.color_options[i] for i in self.color_listbox.curselection()]
            for color in selected_colors:
                color_var_dict = {"vin": self.stored_vin, "color": color}
                nwauto.run_dml("buy_vehicle_colors", color_var_dict)

            self.showbuywarning("Vehicle details and colors successfully added.")
            nwauto.run_unlock()
            self.add_vehicle_window.destroy()
            self.root.destroy()

        except Exception as e:
            nwauto.connection.rollback()
            self.showbuywarning("An error occurred while buying vehicle: {e}")

    def is_float_convertible(self, string):
        try:
            float(string)
            return True
        except ValueError:
            return False
            
    def input_required(self, *args):
        valid = True
        current_year = datetime.now().year
        if len(self.model.get()) > 0:
            self.model_entry.config({"background": "White"})
        else:
            self.model_entry.config({"background": "pink"})
            valid = False

        if len(self.model_year.get()) == 4 and self.model_year.get().isdigit():
            model_year = int(self.model_year.get())
            if model_year <= current_year + 1:
                self.model_year_entry.config({"background": "White"})
            else:
                self.model_year_entry.config({"background": "pink"})
                valid = False
        else:
            self.model_year_entry.config({"background": "pink"})
            valid = False

        if len(self.horsepower.get()) > 0 and len(self.horsepower.get()) < 5 and self.horsepower.get().isdigit():
            self.hp_entry.config({"background": "White"})
        else:
            self.hp_entry.config({"background": "pink"})
            valid = False

        if len(self.purchase_price.get()) > 0 and re.fullmatch(r'\d+(\.\d+)?', self.purchase_price.get()):
            self.price_entry.config({"background": "White"})
        else:
            self.price_entry.config({"background": "pink"})
            valid = False

        selected_colors = [self.color_options[i] for i in self.color_listbox.curselection()]
        if len(selected_colors) <= 0:
            valid = False
            
        if self.vehicle_type.get() == 'Select' or self.manufacturer.get()  == 'Select' or self.fuel_type.get() == 'Select' or self.condition.get() == 'Select':
            valid = False
            
        if len(self.description.get())  > 255:
            var = self.description.get()
            self.desc_entry.delete(0, tk.END)  # Clear existing text
            self.desc_entry.insert(0,var[:255]) # Restrict to 50

        if len(self.model.get())  > 50:
            var = self.model.get()
            self.model_entry.delete(0, tk.END)  # Clear existing text
            self.model_entry.insert(0,var[:50]) # Restrict to 50

        self.submit_button.config(state=tk.NORMAL if valid else tk.DISABLED)
