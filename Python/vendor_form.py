import tkinter as tk
import re
import nwauto  # Importing nwauto to access its functions for database interactions

# Global variable for selected vendor name
vendor_name = ""  # The selected vendor name


# --------------------------------------------------------
# Function to open the Search Vendor Form
# --------------------------------------------------------
def open_search_vendor_form(root, parent_form):
    global vendor_name

    search_window = tk.Toplevel(root)
    x = root.winfo_x()
    y = root.winfo_y()
    search_window.geometry("+%d+%d" % (x + 10, y + 10))
    search_window.transient(root)
    search_window.grab_set()
    search_window.title("Search Vendor")

    tk.Label(search_window, text="Search Vendor", font=("Helvetica", 20, "bold")).pack(pady=10)
    error_label = tk.Label(search_window, text="Enter name", font=("Helvetica", 10, "bold"))
    error_label.pack(pady=5)

    # Vendor name search field
    tk.Label(search_window, text="Vendor Name:").pack(pady=5)
    vendor_check = tk.StringVar()
    vendor_name_entry = tk.Entry(search_window, bg="pink", textvariable=vendor_check)
    vendor_name_entry.pack(pady=5)

    def showwarning(warning):
        error_label["text"] = warning

    def check_vendor(*args):
        if len(vendor_check.get()) > 0:
            vendor_name_entry.config({"background": "white"})
            showwarning("")
        else:
            vendor_name_entry.config({"background": "pink"})
            showwarning("Enter name")

    vendor_check.trace_add(mode=['write'], callback=check_vendor)

    def show_results_window(results):
        # Create a new window for displaying results
        search_window.destroy()
        results_window = tk.Toplevel(root)
        results_window.title("Search Results")
        results_window.geometry("400x300")
        results_window.geometry("+%d+%d" % (x + 10, y + 10))
        results_window.focus()  # Ensure it gets focus immediately
    
        tk.Label(results_window, text="Select a Vendor", font=("Helvetica", 14, "bold")).pack(pady=10)

        frame = tk.Frame(results_window)
        frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Define the select_vendor function outside the loop
        def select_vendor(selected_row):
            global vendor_name
            vendor_name = selected_row[0]
            parent_form.set_vendor(vendor_name)
            results_window.destroy()
            search_window.destroy()

        # Loop through the results and display them
        for row_idx, row in enumerate(results):
            for col_idx, value in enumerate(row):
                tk.Label(scrollable_frame, text=value, borderwidth=1, relief="solid", padx=5, pady=5).grid(row=row_idx, column=col_idx, sticky="nsew")

            # Create a Select button for each row
            tk.Button(scrollable_frame, text="Select", command=lambda r=row: select_vendor(r)).grid(row=row_idx, column=len(row), padx=5, pady=5)

        tk.Button(results_window, text="Close", command=results_window.destroy).pack(pady=10)

    # Search button function
    def search_vendor():
        vendor_name_input = vendor_name_entry.get().strip()
        if not vendor_name_input:
            showwarning("Input Error: Vendor name is required.")
            return

        try:
            # Fetch vendor data from the database
            nwauto.run_lock("find_vendor_lock")
            result = nwauto.get_query_results("find_vendor", {"vendor_name": vendor_name_input})  # Assumes vendor_query.sql exists
            print(result)
            nwauto.run_unlock()

            if result:
                show_results_window(result)  # Show results if more than two rows are returned          
            else:
                showwarning("No vendor found with that name. Try again.")

        except Exception as e:
            showwarning(f"Error while searching vendor: {e}")

    tk.Button(search_window, text="Search Vendors", command=search_vendor).pack(pady=5)
    tk.Button(search_window, text="Cancel", command=search_window.destroy).pack(pady=5)



# --------------------------------------------------------
# Function to open the Add Vendor Form
# --------------------------------------------------------
def open_add_vendor_form(root,parent_form):
    global vendor_name

    if not nwauto.is_position("inventoryclerk"):
        return

    add_window = tk.Toplevel(root)
    x = root.winfo_x()
    y = root.winfo_y()
    add_window.geometry("250x350")
    add_window.geometry("+%d+%d" %(x+10,y+10))
    add_window.transient(root)
    add_window.grab_set()
    add_window.title("Add Vendor")

    tk.Label(add_window, text="Add Vendor", font=("Helvetica", 20, "bold")).grid(row=0,column=0,columnspan=2, padx=5, pady=5, sticky="w")
    error_label = tk.Label(add_window, text="Enter required input", font=("Helvetica", 10, "bold"))
    error_label.grid(row=1,column=0,columnspan=2, padx=5, pady=5, sticky="w")

    # Vendor input fields
    
    state_options = [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME",
        "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA",
        "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
    ]
    state_var = tk.StringVar(value="Select")
    state_dropdown = tk.OptionMenu(add_window, state_var, *state_options)
    submit_button = tk.Button(add_window, text="Submit Vendor")

    #state_dropdown.grid(row=10, column=1, columnspan=3, sticky="we", padx=5, pady=5)
    
    fields = {
        "vendor_name": tk.Entry(add_window, bg="pink"),
        "street_address": tk.Entry(add_window, bg="pink"),
        "city": tk.Entry(add_window, bg="pink"),
        "state": state_dropdown, # tk.Entry(add_window, bg="pink"),
        "postal_code": tk.Entry(add_window, bg="pink"),
        "phone_number": tk.Entry(add_window, bg="pink")
    }

    def check_input(*args):
        phone_pattern = r"^\d{10}$"
        postal_code_pattern = r"^\d{5}$"
        input_good = True
        for inputname in ("vendor_name","street_address","city","postal_code","phone_number"):
            if len(fields[inputname].get()) > 0:
                fields[inputname].config(background="white")
                if inputname == "phone_number" and not re.match(phone_pattern, fields[inputname].get()):
                    fields[inputname].config(background="pink")
                    input_good = False
                if inputname == "postal_code" and not re.match(postal_code_pattern, fields[inputname].get()):
                    fields[inputname].config(background="pink")
                    input_good = False
                if len(fields[inputname].get())  > 50:
                    var = fields[inputname].get()
                    fields[inputname].delete(0, tk.END)  # Clear existing text
                    fields[inputname].insert(0,var[:50]) # Restrict to 50
            else:
                fields[inputname].config(background="pink")
                input_good = False
        if state_var.get() == "Select":
            input_good = False
        submit_button.config(state=tk.NORMAL if input_good else tk.DISABLED)

    state_var.trace_add(mode=['write'], callback=check_input)

    # Display input fields in the form
    r=3
    for label, entry in fields.items():
        tk.Label(add_window, text=label.replace('_', ' ').title() + ":").grid(column=0,row=r, padx=5, pady=5, sticky="w")
        entry.grid(column=1,row=r, padx=5, pady=5, sticky="w")
        entry.bind("<KeyRelease>", check_input)
        r=r+1

    def showwarning(warning):
        error_label["text"]=warning

    # Submit Vendor function
    def submit_vendor():
        # Extract input from fields
        vendor_data = {}
        for field in fields.keys():
            if field == "state":
                vendor_data[field] = state_var.get()
            else:
                vendor_data[field] = fields[field].get().strip()
        #vendor_data = {label: entry.get().strip() for label, entry in fields.items()}

        if not all(vendor_data.values()):
            showwarning("All fields are required.")
            return

        try:
            
            # Verify vendor does not exist
            nwauto.run_lock("find_vendor_lock")
            result = nwauto.get_query_results("find_vendor", {"vendor_name": vendor_data["vendor_name"] })  # Assumes vendor_query.sql exists
            nwauto.run_unlock()
            if result:
                showwarning("Vendor already added.")
                return

            # Insert new vendor data into the database
            vendor_name = ""
            nwauto.run_lock("add_vendor_lock")
            if nwauto.run_dml("add_vendor", vendor_data)  < 0:
                showwarning("Could not add vendor. Try again.")
            else:
                #messagebox.showinfo("Success", f"Vendor '{vendor_data['vendor_name']}' added successfully.")
                vendor_name = vendor_data["vendor_name"]  # Set the selected vendor name globally
                parent_form.set_vendor(vendor_name);
            nwauto.run_unlock()
            if vendor_name != "":
                add_window.destroy()
        
        except Exception as e:
            showwarning(f"Error while adding vendor: {e}")

    # Submit and Back buttons
    submit_button.config(command=submit_vendor)
    submit_button.grid(column=0,row=r, padx=5, pady=5, sticky="w")
    tk.Button(add_window, text="Cancel", command=add_window.destroy).grid(column=1,row=r, padx=5, pady=5, sticky="w")