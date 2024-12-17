# ----------------------------------------------------
# Team041
# Sailesh Arya, Brian Jiang, Aaron Job Ramirez, Nick vanVeldhuisen
# Abstract Code SQL Checks in Python
# Script purpose: Add customer class
# Depends On: tkinger tk/messagebox for forms
#             nwauto.py for MySQL database functions, session variables, etc.
# ----------------------------------------------------

import nwauto
import tkinter as tk
import re
#from tkinter import messagebox

class AddCustomerForm:
    def __init__(self, master, parent_form):
        self.root = master
        self.parent_form =parent_form
        self.root.title("Add Customer Form")
        self.customer_type = tk.StringVar(value="Individual")
        self.customer_type_label = tk.Label(self.root, text="Customer Type:")
        self.customer_type_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.individual_radio = tk.Radiobutton(
            self.root, text="Individual", variable=self.customer_type, value="Individual", command=self.update_form
        )
        self.individual_radio.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.business_radio = tk.Radiobutton(
            self.root, text="Business", variable=self.customer_type, value="Business", command=self.update_form
        )
        self.business_radio.grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.create_common_fields()
        self.create_individual_fields()
        self.create_business_fields()
        self.update_form()
        self.add_button = tk.Button(self.root, text="Add Customer", command=self.add_customer, state="disabled")
        self.add_button.grid(row=15, column=0, columnspan=2, pady=10)
        self.cancel_button = tk.Button(self.root, text="Cancel", command=self.root.destroy)
        self.cancel_button.grid(row=15, column=2, columnspan=2, pady=10)

    def create_common_fields(self):
        self.email_label = tk.Label(self.root, text="Email:")
        self.email_label.grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(row=6, column=1, columnspan=3, sticky="we", padx=5, pady=5)
        self.phone_label = tk.Label(self.root, text="Phone Number:")
        self.phone_label.grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.phone_entry = tk.Entry(self.root, background="pink")
        self.phone_entry.grid(row=7, column=1, columnspan=3, sticky="we", padx=5, pady=5)
        self.street_label = tk.Label(self.root, text="Street Address:")
        self.street_label.grid(row=8, column=0, sticky="w", padx=5, pady=5)
        self.street_entry = tk.Entry(self.root, background="pink")
        self.street_entry.grid(row=8, column=1, columnspan=3, sticky="we", padx=5, pady=5)
        self.city_label = tk.Label(self.root, text="City:")
        self.city_label.grid(row=9, column=0, sticky="w", padx=5, pady=5)
        self.city_entry = tk.Entry(self.root, background="pink")
        self.city_entry.grid(row=9, column=1, columnspan=3, sticky="we", padx=5, pady=5)
        self.state_label = tk.Label(self.root, text="State:")
        self.state_label.grid(row=10, column=0, sticky="w", padx=5, pady=5)
        self.state_options = [
            "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME",
            "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA",
            "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
        ]
        self.state_var = tk.StringVar(value="Select")
        self.state_dropdown = tk.OptionMenu(self.root, self.state_var, *self.state_options)
        self.state_dropdown.grid(row=10, column=1, columnspan=3, sticky="we", padx=5, pady=5)
        self.state_var.trace_add(mode=['write'], callback=self.check_input)
        
        self.postal_label = tk.Label(self.root, text="Postal Code:")
        self.postal_label.grid(row=11, column=0, sticky="w", padx=5, pady=5)
        self.postal_entry = tk.Entry(self.root, background="pink")
        self.postal_entry.grid(row=11, column=1, columnspan=3, sticky="we", padx=5, pady=5)

    def create_individual_fields(self):
        self.first_name_label = tk.Label(self.root, text="First Name:")
        self.first_name_entry = tk.Entry(self.root, background="pink")
        self.last_name_label = tk.Label(self.root, text="Last Name:")
        self.last_name_entry = tk.Entry(self.root, background="pink")
        self.ssn_label = tk.Label(self.root, text="SSN:")
        self.ssn_entry = tk.Entry(self.root, background="pink")

    def create_business_fields(self):
        self.tax_id_label = tk.Label(self.root, text="Business Tax ID:")
        self.tax_id_entry = tk.Entry(self.root, background="pink")
        self.business_name_label = tk.Label(self.root, text="Business Name:")
        self.business_name_entry = tk.Entry(self.root, background="pink")
        self.contact_first_label = tk.Label(self.root, text="Contact First Name:")
        self.contact_first_entry = tk.Entry(self.root, background="pink")
        self.contact_last_label = tk.Label(self.root, text="Contact Last Name:")
        self.contact_last_entry = tk.Entry(self.root, background="pink")
        self.job_title_label = tk.Label(self.root, text="Contact Job Title:")
        self.job_title_entry = tk.Entry(self.root, background="pink")

    def update_form(self):
        if self.customer_type.get() == "Individual":
            self.first_name_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            self.first_name_entry.grid(row=1, column=1, columnspan=3, sticky="we", padx=5, pady=5)
            self.last_name_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
            self.last_name_entry.grid(row=2, column=1, columnspan=3, sticky="we", padx=5, pady=5)
            self.ssn_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
            self.ssn_entry.grid(row=3, column=1, columnspan=3, sticky="we", padx=5, pady=5)
            self.tax_id_label.grid_forget()
            self.tax_id_entry.grid_forget()
            self.business_name_label.grid_forget()
            self.business_name_entry.grid_forget()
            self.contact_first_label.grid_forget()
            self.contact_first_entry.grid_forget()
            self.contact_last_label.grid_forget()
            self.contact_last_entry.grid_forget()
            self.job_title_label.grid_forget()
            self.job_title_entry.grid_forget()
        else:
            self.tax_id_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            self.tax_id_entry.grid(row=1, column=1, columnspan=3, sticky="we", padx=5, pady=5)
            self.business_name_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
            self.business_name_entry.grid(row=2, column=1, columnspan=3, sticky="we", padx=5, pady=5)
            self.contact_first_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
            self.contact_first_entry.grid(row=3, column=1, columnspan=3, sticky="we", padx=5, pady=5)
            self.contact_last_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
            self.contact_last_entry.grid(row=4, column=1, columnspan=3, sticky="we", padx=5, pady=5)
            self.job_title_label.grid(row=5, column=0, sticky="w", padx=5, pady=5)
            self.job_title_entry.grid(row=5, column=1, columnspan=3, sticky="we", padx=5, pady=5)
            self.first_name_label.grid_forget()
            self.first_name_entry.grid_forget()
            self.last_name_label.grid_forget()
            self.last_name_entry.grid_forget()
            self.ssn_label.grid_forget()
            self.ssn_entry.grid_forget()
        for entry in [
            self.phone_entry, self.street_entry, self.city_entry, self.postal_entry,
            self.first_name_entry, self.last_name_entry, self.ssn_entry,
            self.tax_id_entry, self.business_name_entry, self.contact_first_entry, self.contact_last_entry,self.job_title_entry, self.email_entry
        ]:
            entry.bind("<KeyRelease>", self.check_input)

    def check_input(self, *args):
        ssn_pattern = r"^\d{9}$"
        phone_pattern = r"^\d{10}$"
        tax_id_pattern = r"^\d{2}-\d{7}$"
        postal_code_pattern = r"^\d{5}$"
        required_entries = [self.phone_entry, self.street_entry, self.city_entry, self.postal_entry]

        if self.customer_type.get() == "Individual":
            required_entries += [self.first_name_entry, self.last_name_entry, self.ssn_entry]
        else:
            required_entries += [self.tax_id_entry, self.business_name_entry, self.contact_first_entry, self.contact_last_entry, self.job_title_entry]

        all_filled = True
        for entry in required_entries:
            value = entry.get().strip()
            if entry == self.ssn_entry and self.customer_type.get() == "Individual":
                if re.match(ssn_pattern, value):
                    entry.config(background="white")
                else:
                    entry.config(background="pink")
                    all_filled = False
            elif entry == self.phone_entry:
                if re.match(phone_pattern, value):
                    entry.config(background="white")
                else:
                    entry.config(background="pink")
                    all_filled = False
            elif entry == self.tax_id_entry and self.customer_type.get() == "Business":
                if re.match(tax_id_pattern, value):
                    entry.config(background="white")
                else:
                    entry.config(background="pink")
                    all_filled = False
            elif entry == self.postal_entry:
                if re.match(postal_code_pattern, value):
                    entry.config(background="white")
                else:
                    entry.config(background="pink")
                    all_filled = False
            elif not value:
                entry.config(background="pink")
                all_filled = False
            else:
                entry.config(background="white")
            if len(value) > 50:
                entry.delete(0, tk.END)  # Clear existing text
                entry.insert(0,value[:50]) # Restrict to 50

        if len(self.email_entry.get())  > 50:
            var = self.email_entry.get()
            self.email_entry.delete(0, tk.END)  # Clear existing text
            self.email_entry.insert(0,var[:50]) # Restrict to 50

        if self.state_var.get() == "Select":
            all_filled = False
        

        self.add_button.config(state="normal" if all_filled else "disabled")

    def add_customer(self):
        successful = False
        try:
            customer_data = {
                "email": self.email_entry.get(),
                "phone_number": self.phone_entry.get(),
                "street_address": self.street_entry.get(),
                "city": self.city_entry.get(),
                "state": self.state_var.get(),
                "postal_code": self.postal_entry.get(),
            }
            nwauto.run_lock("add_customer_lock")
            customer_id = nwauto.run_dml("add_customer", customer_data)

            if self.customer_type.get() == "Individual":
                individual_data = {
                    "ssn": self.ssn_entry.get(),
                    "first_name": self.first_name_entry.get(),
                    "last_name": self.last_name_entry.get(),
                }
                nwauto.run_dml("add_customer_individual", individual_data)
                #messagebox.showinfo("Success", "Individual customer added successfully.")
                print("Individual customer added successfully.")
                self.parent_form.set_customer(customer_id,f"{individual_data['first_name']} {individual_data['last_name']}")
                self.parent_form.showwarning("Individual added. Customer selected.")
                successful = True
            else:
                business_data = {
                    "business_tax_id": self.tax_id_entry.get(),
                    "business_name": self.business_name_entry.get(),
                    "contact_firstname": self.contact_first_entry.get(),
                    "contact_lastname": self.contact_last_entry.get(),
                    "contact_job_title": self.job_title_entry.get(),
                }
                nwauto.run_dml("add_customer_business", business_data)
                #messagebox.showinfo("Success", "Business customer added successfully.")
                print("Business customer added successfully.")
                self.parent_form.set_customer(customer_id,f"{business_data['business_name']}")
                self.parent_form.showwarning("Business added. Customer selected.")
                successful = True
        
        except Error as e:
            print(e)

        # Make sure we unlock, success or failure
        nwauto.run_unlock()

        # If success, parent form should have what it needs
        if successful:
            self.root.destroy() # 
