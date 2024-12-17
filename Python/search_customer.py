# ----------------------------------------------------
# Team041
# Sailesh Arya, Brian Jiang, Aaron Job Ramirez, Nick vanVeldhuisen
# Python Class
# Class purpose: search customer form
# Depends On: TK for forms, nwauto.py for MySQL functions 
# ----------------------------------------------------


import nwauto
import tkinter as tk
import re

class SearchCustomerForm:
    def __init__(self, master, parent_form):
        self.root = master
        self.parent_form = parent_form
        self.customer_record = {"customer_id": -1, "customer_name": ""}
        self.root.title("Search Customer")
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
        self.create_input_fields()
        self.update_form()
        self.submit_button = tk.Button(self.root, text="Submit", command=self.search_customer)
        self.submit_button.grid(row=4, column=1, pady=10)
        self.submit_button.config(state="disabled")
        self.cancel_button = tk.Button(self.root, text="Cancel", command=self.cancel_search)
        self.cancel_button.grid(row=4, column=2, pady=10)
        self.result_label = tk.Label(self.root, text="", justify="left")
        self.choose_customer_button = tk.Button(self.root, text="Select", command=self.select_customer, state="disabled")
        self.choose_customer_button.grid(row=4, column=3, padx=5, pady=5)
        self.error_label = tk.Label(self.root, text=f"Submit to search. Select to choose", font=("Helvetica", 10, "normal"))
        self.error_label.grid(row=5, column=0, columnspan=4, padx=5, pady=5)

    def showwarning(self,warning):
        self.error_label["text"]=warning

    def clearwarning(self):
        self.error_label["text"]=""

    def create_input_fields(self):
        self.ssn_label = tk.Label(self.root, text="SSN:")
        self.ssn_entry = tk.Entry(self.root)
        self.tax_id_label = tk.Label(self.root, text="Business Tax ID:")
        self.tax_id_entry = tk.Entry(self.root)

    def update_form(self):
        if self.customer_type.get() == "Individual":
            self.ssn_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            self.ssn_entry.grid(row=1, column=1, columnspan=2, sticky="we", padx=5, pady=5)
            self.ssn_entry.config({"background": "pink"})
            self.tax_id_label.grid_forget()
            self.tax_id_entry.grid_forget()
        else:
            self.tax_id_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
            self.tax_id_entry.grid(row=1, column=1, columnspan=2, sticky="we", padx=5, pady=5)
            self.tax_id_entry.config({"background": "pink"})
            self.ssn_label.grid_forget()
            self.ssn_entry.grid_forget()

        self.ssn_entry.bind("<KeyRelease>", self.check_input)
        self.tax_id_entry.bind("<KeyRelease>", self.check_input)

    def check_input(self, event):
        if self.customer_type.get() == "Individual":
            if self.ssn_entry.get().strip():
                self.ssn_entry.config({"background": "white"})
                self.submit_button.config(state="normal")
            else:
                self.ssn_entry.config({"background": "pink"})
                self.submit_button.config(state="disabled")
        elif self.customer_type.get() == "Business":
            if self.tax_id_entry.get().strip():
                self.tax_id_entry.config({"background": "white"})
                self.submit_button.config(state="normal")
            else:
                self.tax_id_entry.config({"background": "pink"})
                self.submit_button.config(state="disabled")

    def is_valid_ssn(self, ssn):
        return re.match(r'^\d{9}$', ssn)

    def is_valid_tax_id(self, tax_id):
        return re.match(r'^\d{2}-\d{7}$', tax_id)

    def search_customer(self):
        try:
            if self.customer_type.get() == "Individual":
                ssn = self.ssn_entry.get().strip()
                if not self.is_valid_ssn(ssn):
                    self.showwarning("Invalid SSN format. Please use #########.")
                    return
                nwauto.run_lock("find_customer_individual_lock")
                customer_data = nwauto.get_query_results("find_customer_individual", {"ssn": ssn})
                if not customer_data:
                    self.choose_customer_button.config(state="disabled")
                    self.showwarning("Individual customer not found.")
                else:
                    customer_rec = customer_data[0]
                    self.display_individual_result(customer_rec)
                    self.choose_customer_button.config(state="normal")
            else:
                tax_id = self.tax_id_entry.get().strip()
                if not self.is_valid_tax_id(tax_id):
                    self.showwarning("Invalid Business Tax ID format. Please use ##-#######.")
                    return
                nwauto.run_lock("find_customer_business_lock")
                customer_data = nwauto.get_query_results("find_customer_business", {"business_tax_id": tax_id})
                print(customer_data)
                if not customer_data:
                    self.choose_customer_button.config(state="disabled")
                    self.showwarning("Business customer not found.")
                else:
                    customer_rec = customer_data[0]
                    self.display_business_result(customer_rec)
                    self.choose_customer_button.config(state="normal")
        except Error as e:
            print(e)
        nwauto.run_unlock()

    def display_individual_result(self, record):
        result_text = (
            f"First Name: {record[6]}\n"
            f"Last Name: {record[7]}\n"
            f"SSN: {record[8]}\n"
            f"Street Address: {record[0]}, {record[1]}, {record[2]}, {record[3]}\n"
            f"Phone Number: {record[4]}\n"
            f"Email: {record[5] if record[5] else 'N/A'}\n"
            f"Customer_Id: {record[9]}\n"
        )
        self.customer_record["customer_name"] = f"{record[6]} {record[7]}"
        self.customer_record["customer_id"] = record[9]
        self.show_result(result_text)

    def display_business_result(self, record):
        result_text = (
            f"Business Name: {record[6]}\n"
            f"Contact: {record[8]} {record[9]}\n"
            f"Job Title: {record[10]}\n"
            f"Business Tax ID: {record[7]}\n"
            f"Street Address: {record[0]}, {record[1]}, {record[2]}, {record[3]}\n"
            f"Phone Number: {record[4]}\n"
            f"Email: {record[5] if record[5] else 'N/A'}\n"
            f"Customer_Id: {record[11]}\n"
        )
        self.customer_record["customer_name"] = f"{record[6]}"
        self.customer_record["customer_id"] = record[11]
        self.show_result(result_text)

    def show_result(self, result_text):
        self.result_label.config(text=result_text)
        self.result_label.grid(row=6, column=0, columnspan=4, padx=5, pady=5)
        self.showwarning("Customer found. Click Select to choose.")

    def select_customer(self):
        self.parent_form.set_customer(self.customer_record["customer_id"],self.customer_record["customer_name"]) 
        self.parent_form.showwarning("Customer selected.")
        self.root.destroy()

    def cancel_search(self):
        self.root.destroy()
