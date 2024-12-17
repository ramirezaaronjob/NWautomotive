# ----------------------------------------------------
# Team041
# Sailesh Arya, Brian Jiang, Aaron Job Ramirez, Nick vanVeldhuisen
# Python Class vehicle_parts_order_form.VehiclePartsForm
# Class purpose: Vehicle Parts Order Form
# Depends On: tkinger tk/tkk for forms
#             nwauto.py for MySQL database functions, session variables, etc.
#             vendor_form.py for Vendor add/search forms
# Called By: vehicle_search.py Vehicle Info button
# ----------------------------------------------------

import tkinter as tk
import nwauto
from vendor_form import open_add_vendor_form, open_search_vendor_form
import re




# Function to fetch and display vehicle parts for a specific VIN
# def fetch_vehicle_parts(vin):
#     try:
#         var_dict = {"vin": vin}
#         nwauto.run_lock("get_next_order_number_for_vin_lock")
#         parts_data = nwauto.get_query_results("get_next_order_number_for_vin", var_dict)
#         nwauto.run_unlock()
#         print(parts_data)
        
#         if not parts_data:
#             messagebox.showinfo("No Data", f"No parts found for VIN: {vin}")
#             return []
        
#         return parts_data
#     except Exception as e:
#         print(f"Error fetching vehicle parts: {e}")
#         messagebox.showerror("Error", f"An error occurred while fetching vehicle parts: {e}")
#         return []



global_part_row_count = 0

# Class to create the Vehicle Parts Form
class VehiclePartsForm:
    def __init__(self, master, vin, parent_form):
        self.master = master
        self.parent_form = parent_form
        self.vin = vin  # Store VIN as an instance variable
        self.vendor_name = ""
        self.master.title("Vehicle Parts Form")
        self.master.geometry("880x600")
        # self.display_parts

        # Display the VIN in a label for confirmation
        self.vin_label = tk.Label(master, text=f"VIN: {self.vin}", font=("Helvetica", 14, "bold"))
        self.vin_label.grid(row=0, column=0, padx=5, pady=5, sticky="w", columnspan=4)
        self.vendor_label = tk.Label(master, text=f"Select Vendor", font=("Helvetica", 14, "bold"))
        self.vendor_label.grid(row=0, column=4, padx=5, pady=5, sticky="w", columnspan=4)

        # Search vendor form button
        self.search_vendor_form_button = tk.Button(master, text="Search Vendor", command=self.search_vendor)
        self.search_vendor_form_button.grid(row=1, column=0, pady=5, sticky="w")  # Placed in row 2
        
        # Vendor form button
        self.add_vendor_form_button = tk.Button(master, text="Add Vendor", command=self.add_vendor)
        self.add_vendor_form_button.grid(row=1, column=2,  pady=5, sticky="w")

        # Add part button
        self.add_part_button = tk.Button(master, text="Add Part", command=self.add_part_row)
        self.add_part_button.grid(row=1, column=4, pady=5, sticky="w")
        self.add_part_button.config(state="disabled")

        # List to hold part input fields
        self.part_entries = []

        # Submit button
        self.submit_button = tk.Button(master, text="Submit Parts Order", command=self.submit_parts_order)
        self.submit_button.grid(row=1, column=6, pady=5, sticky="w")
        self.submit_button.config(state="disabled")

        # Error message display
        self.error_label = tk.Label(master, text=f"", font=("Helvetica", 14, "bold"))
        self.error_label.grid(row=2, column=0, columnspan=8, pady=5, sticky="w")

    def showwarning(self,warning):
        self.error_label["text"]=warning

    def clearwarning(self):
        self.error_label["text"]=""
        
    def set_vendor(self,name):
        self.vendor_label["text"]="VENDOR:"+name
        self.vendor_name=name
        self.add_part_button.config(state="normal")

    def add_vendor(self):
        open_add_vendor_form(self.master, self)

    def search_vendor(self):
        open_search_vendor_form(self.master, self)

    # # Function to display parts data in the form
    # def display_parts(self):
    #     parts_data = fetch_vehicle_parts(self.vin)
    #     if parts_data:
    #         for part in parts_data:
    #             self.add_part_row(part_data=part)

    # Function to add a new row for part entry
    def add_part_row(self):
        self.showwarning("Complete required input for all parts: Vendor Name Price (#.#) Quantity(#) Description")

        # Create a new frame for the part entry
        part_frame = tk.Frame(self.master)
        part_frame.grid(row=len(self.part_entries) + 4, column=0, columnspan=8, pady=5, padx=10)

        global global_part_row_count

        # Increment the row count
        global_part_row_count += 1

        # Vendor Part Number field
        vendor_part_label = tk.Label(part_frame, text="Vendor Part Number:")
        vendor_part_label.grid(row=0, column=0)
        vendor_part_check = tk.StringVar()  # Unused
        vendor_part_entry = tk.Entry(part_frame, textvariable=vendor_part_check, bg="pink")
        vendor_part_entry.grid(row=0, column=1)

        # Unit Price field
        unit_price_label = tk.Label(part_frame, text="Unit Price:")
        unit_price_label.grid(row=0, column=2)
        unit_price_check = tk.StringVar()  # Unused
        unit_price_entry = tk.Entry(part_frame, textvariable=unit_price_check, bg="pink")
        unit_price_entry.grid(row=0, column=3)

        # Quantity field
        quantity_label = tk.Label(part_frame, text="Quantity:")
        quantity_label.grid(row=0, column=4)
        quantity_check = tk.StringVar()  # Unused
        quantity_entry = tk.Entry(part_frame, textvariable=quantity_check, bg="pink")
        quantity_entry.grid(row=0, column=5)

        # Description field
        description_label = tk.Label(part_frame, text="Description:")
        description_label.grid(row=0, column=6)
        description_check = tk.StringVar()  # Unused
        description_entry = tk.Entry(part_frame, textvariable=description_check, bg="pink")
        description_entry.grid(row=0, column=7)

        # Delete button for the row
        delete_button = tk.Button(part_frame, text="Delete", command=lambda: self.delete_part_row(part_frame))
        delete_button.grid(row=0, column=8, padx=5)

        # Tracking the part entry details
        self.part_entries.append({
            "frame": part_frame,
            "vendor_part": vendor_part_entry, "vendor_part_check": vendor_part_check,
            "unit_price": unit_price_entry, "unit_price_check": unit_price_check,
            "quantity": quantity_entry, "quantity_check": quantity_check,
            "description": description_entry, "description_check": description_check,
            "delete_button": delete_button
        })

        vendor_part_check.trace_add(mode=['write'], callback=self.input_required)
        unit_price_check.trace_add(mode=['write'], callback=self.input_required)
        quantity_check.trace_add(mode=['write'], callback=self.input_required)
        description_check.trace_add(mode=['write'], callback=self.input_required)



    # Load existing part data if provided (not requirement but keeping code because it looks great)
# if part_data:
#     vendor_part_entry.insert(0, part_data[0])
#     unit_price_entry.insert(0, part_data[1])
#     quantity_entry.insert(0, part_data[2])
#     description_entry.insert(0, part_data[3])

# Trace functions to monitor changes (but not recommended to read values directly due to infinite loop risk)
# vendor_part_check.trace_add(mode=['write'], callback=self.input_required) # READ WILL CAUSE INFINITE LOOP!!!!
# unit_price_check.trace_add(mode=['write'], callback=self.input_required) # READ WILL CAUSE INFINITE LOOP!!!!
# quantity_check.trace_add(mode=['write'], callback=self.input_required) # READ WILL CAUSE INFINITE LOOP!!!!
# description_check.trace_add(mode=['write'], callback=self.input_required) # READ WILL CAUSE INFINITE LOOP!!!!
        

    def delete_part_row(self, part_frame):
        global global_part_row_count
        global valid 
        valid = False
        # Decrement the row count
        global_part_row_count -= 1
        print(global_part_row_count)
        # Remove the part frame from the grid
        part_frame.grid_forget()

        # Remove the part entry details from the part_entries list
        self.part_entries = [entry for entry in self.part_entries if entry["frame"] != part_frame]
        self.input_required()

    def submit_parts_order(self):
        parts_data = []
        for entry in self.part_entries:
            vendor_part_number = entry["vendor_part"].get()
            unit_price = entry["unit_price"].get()
            quantity = entry["quantity"].get()
            description = entry["description"].get()

            if not vendor_part_number or not unit_price or not quantity:
                self.showwarning("Input Error", "Vendor Part Number, Unit Price, and Quantity are required.")
                return

            try:
                unit_price = float(unit_price)
                quantity = int(quantity)
            except ValueError:
                self.showwarning("Input Error", "Unit Price must be a number and Quantity must be an integer.")
                return

            parts_data.append((vendor_part_number, unit_price, quantity, description))

        try:
            # Using the VIN as the order number just for example; replace with your logic if needed
            var_dict = {"vin": self.vin}
            nwauto.run_lock("get_next_order_number_for_vin_lock")
            next_order = nwauto.get_query_results("get_next_order_number_for_vin", var_dict)
            nwauto.run_unlock()

# Extract '005' from next_order, assuming it's structured as [('005',)]
            if next_order and next_order[0]:  # Check if next_order is not empty
                next_order_str = next_order[0][0]  # Access the first element of the first tuple
                order_number = f"{str(self.vin)}-{next_order_str}"
            else:
    # Handle the case where next_order is empty or unexpected
                order_number = f"{str(self.vin)}-001"  # Default or fallback value
            parts_order_dict = {
                    "order_number": order_number,
                    "vin": str(self.vin),
                    "vendor_name": self.vendor_name
                }
            nwauto.run_lock("insert_parts_order_lock")
            if nwauto.run_dml("insert_parts_order", parts_order_dict) < 0:
                self.showwarning("Could not create parts order. Check your input and try again or contact technical support.")
                return # Leaves a dead parts order fornow
            else:
                self.showwarning("Parts Order created successfully.")
                self.search_vendor_form_button.config(state="disabled") # Committed to vendor
                self.add_vendor_form_button.config(state="disabled") # Committed to vendor
            nwauto.run_unlock()

            for part in parts_data:
                #vendor_part_number, unit_price, quantity, description
                print(part)
                values_dict = {
                    "vendor_part_number": part[0],
                    "order_number": order_number,
                    "vendor_name": self.vendor_name,
                    "vin": self.vin,
                    "description": part[3],
                    "unit_price": str(part[1]),  # Convert to string
                    "quantity": str(part[2])       # Convert to string
                }
                print (values_dict)
                # Run the query with formatted values
                nwauto.run_lock("insert_parts_lock")
                if nwauto.run_dml("insert_parts", values_dict) < 0:
                    self.showwarning("Could not add a vendor part to the order. Check your input and try again or contact technical support.")
                    nwauto.run_unlock()
                    return
                nwauto.run_unlock()

            self.parent_form.load_grid() # Rebuild form
            self.master.destroy() # Close

        except Exception as e:
            print(f"Error: {e}")
            self.showwarning("An error occurred while submitting parts order: {e}")

    def input_required(self, *args):
       try:
           global valid
           valid = True
           vendor_partnum_list = []

           warning = "Complete required input for all parts: "
           if global_part_row_count <= 0:
               valid = False
               #warning = "At least one part must be added."
           # Validate inputs if there are rows
           if global_part_row_count > 0:
               for entry in self.part_entries:
                   vendor_part_number = entry["vendor_part_check"].get()
                   vendor_partnum_list.append(vendor_part_number)
                   unit_price = entry["unit_price_check"].get()
                   quantity = entry["quantity_check"].get()
                   description = entry["description_check"].get()

                   # Validate Vendor Part Number
                   if len(vendor_part_number) > 0:
                        entry["vendor_part"].config({"background": "White"})
                        if len(vendor_part_number) > 50:
                            entry["vendor_part"].delete(0, tk.END)  # Clear existing text
                            entry["vendor_part"].insert(0,vendor_part_number[:50]) # Restrict to 50
                   else:
                       entry["vendor_part"].config({"background": "pink"})
                       warning += " Vendor Part Number"
                       valid = False

                   # Validate Unit Price
                   if len(unit_price) > 0 and re.fullmatch(r'\d+(\.\d+)?', unit_price):
                       entry["unit_price"].config({"background": "White"})
                   else:
                       entry["unit_price"].config({"background": "pink"})
                       warning += " Unit Price (#.#)"
                       valid = False

                   # Validate Quantity
                   if len(quantity) > 0 and quantity.isdigit():
                       entry["quantity"].config({"background": "White"})
                   else:
                       entry["quantity"].config({"background": "pink"})
                       warning += " Quantity (#)"
                       valid = False

                   # Validate Description
                   if len(description) > 0:
                        entry["description"].config({"background": "White"})
                        if len(description) > 50:
                            entry["description"].delete(0, tk.END)  # Clear existing text
                            entry["description"].insert(0,description[:50]) # Restrict to 50
                   else:
                       entry["description"].config({"background": "pink"})
                       warning += " Description"
                       valid = False

           
           # Show warning or clear it
           if valid:
               self.clearwarning()
           else:
               self.showwarning(warning)

           # Log diagnostics
           #print(f"Global Part Row Count: {global_part_row_count}")
           #print(f"Is Valid: {valid}")

           # Check for duplicate part numbers
           if len(vendor_partnum_list) != len(set(vendor_partnum_list)):
               valid = False
               self.showwarning("You have a duplicate part # in the list!")
               
           # Enable/disable submit button based on validation
           self.submit_button.config(state=tk.NORMAL if valid and global_part_row_count > 0 else tk.DISABLED)

       except Exception as e:
           print(f"Error: {e}")
           self.showwarning(f"An error occurred during validation: {e}")


