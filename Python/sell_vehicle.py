# ----------------------------------------------------
# Team041
# Sailesh Arya, Brian Jiang, Aaron Job Ramirez, Nick vanVeldhuisen
# Python Class sell_vehicle.SellVehicleForm
# Class purpose: Sell Vehicle to customer
# Depends On: tkinger tk/tkk for forms
#             nwauto.py for MySQL database functions, session variables, etc.
#             search_customer.py for Customer search form (shared with Buy Vehicle)
#             add_customer.py for Customer Add form (shared with Buy Vehicle)
# Called By: vehicle_search.py Vehicle Info button
# ----------------------------------------------------

import nwauto
import tkinter as tk
from add_customer import AddCustomerForm
from search_customer import SearchCustomerForm
#from datetime import datetime

class SellVehicleForm:
    def __init__(self, master, vin, parent_form):
        self.root = master
        self.parent_form = parent_form
        self.customer_id = -1
        self.root.title("Sell Vehicle Form")
        self.vin = vin 
        self.vin_label = tk.Label(master, text=f"VIN: {self.vin}", font=("Helvetica", 14, "bold"))
        self.vin_label.grid(row=0, columnspan=4, column=0, padx=10, pady=10)
        self.customer_label = tk.Label(master, text=f"Search/Add Customer", font=("Helvetica", 14, "bold"))
        self.customer_label.grid(row=1, columnspan=4, column=0, padx=10, pady=10)
        self.search_customer_button = tk.Button(self.root, text="Search Customer", command=self.search_customer, state="normal")
        self.search_customer_button.grid(row=2, column=0, padx=5, pady=5)
        self.add_customer_button = tk.Button(self.root, text="Add Customer", command=self.add_customer, state="normal")
        self.add_customer_button.grid(row=2, column=1, padx=5, pady=5)
        self.sell_vehicle_button = tk.Button(self.root, text="Sell Vehicle", state="disabled", command=self.process_sale)
        self.sell_vehicle_button.grid(row=2, column=2, padx=5, pady=5)
        self.cancel_button = tk.Button(self.root, text="Cancel", command=self.root.destroy)
        self.cancel_button.grid(row=2, column=3, padx=5, pady=5)
        # Error message display
        self.error_label = tk.Label(master, text=f"Select Customer", font=("Helvetica", 10, "normal"))
        self.error_label.grid(row=3, column=0, columnspan=4, pady=5, sticky="w")
    
    def showwarning(self,warning):
        self.error_label["text"]=warning

    def set_customer(self, i, name): 
        self.customer_id = i
        self.customer_label["text"] = name
        self.sell_vehicle_button.config(state="normal")

    def search_customer(self):
        self.search_window = tk.Toplevel(self.root)
        self.search_window.transient(self.root)
        self.search_window.grab_set() # Make child window modal!
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        self.search_window.geometry("+%d+%d" %(x+10,y+10))
        SearchCustomerForm(self.search_window, self)

    def add_customer(self):
        self.add_window = tk.Toplevel(self.root)
        self.add_window.transient(self.root)
        self.add_window.grab_set() # Make child window modal!
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        self.add_window.geometry("+%d+%d" %(x+10,y+10))
        AddCustomerForm(self.add_window, self)

    def process_sale(self):
        successful = False

        if not self.customer_id > 0: # VIN set from caller already...should not be able to get here
            self.showwarning("Search or Add Customer for Vehicle Sale.")
            return

        var_dict = {
             # "sale_date" : datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Set by SQL
             "vin" : self.vin
            ,"customer_id" : str(self.customer_id) # .get()
            ,"username" : nwauto.get_username()
        }
        try:
            nwauto.run_lock("sell_vehicle_lock")
            nwauto.run_dml("sell_vehicle",var_dict)
            successful = True
        except Exception as e:
            nwauto.connection.rollback()
            self.showwarning("Transaction Error {e}")

        nwauto.run_unlock()
        if successful:
            self.parent_form.vehicle_label.config(text="THIS VEHICLE HAS BEEN SOLD!")
            self.parent_form.part_received_button.config(state="disabled")
            self.parent_form.part_installed_button.config(state="disabled")
            self.parent_form.load_grid() 
            self.root.destroy() 
