# ----------------------------------------------------
# Team041
# Sailesh Arya, Brian Jiang, Aaron Job Ramirez, Nick vanVeldhuisen
# Class purpose: Vehicle search class / main program
# Depends On: tkinger tk/tkk for forms
#             nwauto.py for MySQL database functions, session variables, etc.
#             login_form.py for User Login form
#             info_form.py for Vehicle Info form
#             reports.py for Vehicle Info form
# Called By: Main program startup
# ----------------------------------------------------

import nwauto
import login_form
import info_form
import reports
import tkinter as tk
from tkinter import ttk, font
import buy_vehicle
from datetime import datetime
import re

# ---------
# Constants
# ---------
# Public search result column names and indexes
c_v="VIN#"
k_v=0
c_vt="Vehicle Type"
k_vt=1
c_mn="Manufacturer"
k_mn=2
c_md="Model"
k_md=3
c_y="Year"
k_y=4
c_f="Fuel Type"
k_f=5
c_c="Colors(s)"
k_c=6
c_h="Horsepower"
k_h=7
c_ask="Sale Price"
k_ask=8
# Not shown by default - Must be logged in as Privileged user
c_st="Status"
k_st=9
c_pp="Parts?"
k_pp=10

class vehicle_search_form:
        def __init__(self,root):

                # Search startup content
                self.manufacturers = []
                self.colors = []
                self.vehicle_type = []
                self.vehicles_available = []
                self.vehicles_pending = []
                self.vehicle_search_results = []
                self.sale_status_choice = []
                self.var_dict = {}
                self.vehicles_available_text = ""
                self.vehicles_pending_text = ""
                
                # Read lookups from database
                try:
                        self.populate_lookups() # Called once
                except Error as e:
                        print(e)
                        
                self.root = root
                self.root.title("Vehicle Search Form")

                self.keyword_label = tk.Label(root, text="Keyword:", anchor="w")
                self.keyword_label.grid(row=0, column=0, sticky='w')
                self.keyword_entry = tk.Entry(root)
                self.keyword_entry.focus_set() # PUT CURSOR ON KEYWORD (CAN ALTER LATER)
                self.keyword_entry.grid(row=0, column=1, sticky='w')
                self.keyword_entry.bind("<Return>", self.vehicle_search_caller)

                # Create but do not place unless logged in
                self.vin_label = tk.Label(root, text="Vin#:", anchor="w")
                self.vin_entry = tk.Entry(root)
                self.vin_entry.bind("<Return>", self.vehicle_search_caller)

                self.manufacturer_label = tk.Label(root, text="Manufacturer:", anchor="w")
                self.manufacturer_label.grid(row=0, column=2, sticky='w')
                self.manufacturer_choice = tk.StringVar()
                self.manufacturer_choice.set( "All" )
                self.manufacturer_options = self.get_dropdown(self.manufacturers)
                self.manufacturer_optionmenu = tk.OptionMenu(root, self.manufacturer_choice, *self.manufacturer_options)
                self.manufacturer_optionmenu.grid(row=0, column=3, sticky='w')

                self.vehicletype_label = tk.Label(root, text="Vehicle Type:", anchor="w")
                self.vehicletype_label.grid(row=1, column=2, sticky='w')
                self.vehicletype_choice = tk.StringVar()
                self.vehicletype_choice.set( "All" )
                self.vehicletype_options = self.get_dropdown(self.vehicle_type)
                self.vehicletype_optionmenu = tk.OptionMenu(root, self.vehicletype_choice, *self.vehicletype_options)
                self.vehicletype_optionmenu.grid(row=1, column=3, sticky='w')

                self.color_label = tk.Label(root, text="Color:", anchor="w")
                self.color_label.grid(row=0, column=4, sticky='w')
                self.color_choice = tk.StringVar()
                self.color_choice.set( "All" )
                self.color_options = self.get_dropdown(self.colors)
                self.color_optionmenu = tk.OptionMenu(root, self.color_choice, *self.color_options)
                self.color_optionmenu.grid(row=0, column=5, sticky='w')

                self.fueltype_label = tk.Label(root, text="Fuel Type:", anchor="w")
                self.fueltype_label.grid(row=1, column=4, sticky='w')
                self.fueltype_choice = tk.StringVar()
                self.fueltype_choice.set( "All" )
                print(self.fuel_type)
                self.fueltype_options = self.get_dropdown(self.fuel_type) #["All","Gas","Diesel","Natural Gas","Hybrid","Plugin Hybrid","Battery","Fuel Cell"]
                print(self.fueltype_options)
                #Gas, Diesel, Natural Gas, Hybrid, Plugin Hybrid, Battery, Fuel Cell
                self.fueltype_optionmenu = tk.OptionMenu(root, self.fueltype_choice, *self.fueltype_options)
                self.fueltype_optionmenu.grid(row=1, column=5, sticky='w')
                
                self.year_label = tk.Label(root, text="Year:", anchor="w")
                self.year_label.grid(row=0, column=6, sticky='w')
                self.year_entry = tk.Entry(root, width=4)
                self.year_entry.bind("<Return>", self.vehicle_search_caller)
                self.year_entry.bind("<KeyRelease>", self.check_input)
                self.year_entry.grid(row=0, column=7, sticky='w')

                self.search_button = tk.Button(root, text="Search", command=self.vehicle_search)
                self.search_button.grid(row=1, column=8, sticky='w')

                self.login_button = tk.Button(root, text="Login", command=self.login_form)
                self.login_button.grid(row=0, column=8, sticky='w')
                self.position_label = tk.Label(root, text="Z", anchor="w")
                self.position_label["text"]="Public Search" # Updated to logged in user by login form (should do through function here though)
                self.position_label.grid(row=5, column=8, sticky='w')
                
                # Public search grid (rebuilt on login form)
                self.vehicle_columns=(c_v, c_vt, c_mn, c_md, c_y, c_f, c_c, c_h, c_ask)
                self.results_tree = ttk.Treeview(root, columns=self.vehicle_columns, show="headings")
                
                # Default search for vehicle on startup to have no VIN#
                self.curVin = ""

                # Get info button (currently not enabled on selection but should be)
                self.info_button = tk.Button(root, text="Get Vehicle Details", command=self.get_vehicle, state="disabled")
                self.info_button.grid(row=5, column=0, sticky='w')
                # Display of vehicles available (always show)
                self.vehicles_available_label = tk.Label(root, text= self.vehicles_available_text, anchor="w")
                self.vehicles_available_label.grid(row=5, column=2, sticky='w')

                # Hidden Privileged things
                # Status search
                self.salestatus_label = tk.Label(root, text="Status:", anchor="w")
                self.salestatus_choice = tk.StringVar()
                self.salestatus_choice.set( "All" )
                self.salestatus_options = self.get_dropdown(self.sale_status_choice)
                self.salestatus_optionmenu = tk.OptionMenu(root, self.salestatus_choice, *self.salestatus_options)
                # Reports form launch
                self.reports_menu_button = tk.Menubutton(root, text="Reports", relief=tk.RAISED)
                self.reports_menu = tk.Menu(self.reports_menu_button, tearoff=0)
                self.reports_menu_button.configure(menu=self.reports_menu)
                self.reports_menu.add_command(label="Seller History", command=self.open_seller_history_report)
                self.reports_menu.add_command(label="Average Time in Inventory", command=self.open_avg_time_inventory_report)
                self.reports_menu.add_command(label="Price Per Condition", command=self.open_price_per_condition_report)
                self.reports_menu.add_command(label="Parts Statistics", command=self.open_parts_statistics_report)
                self.reports_menu.add_command(label="Monthly Sales", command=self.open_monthly_sales_report)

                # Add vehicle form launch
                self.addvehicle_button = tk.Button(root, text="Add Vehicle", command=self.add_vehicle)
                # Vehicles pending display
                self.vehicles_pending_label = tk.Label(root, text=self.vehicles_pending_text, anchor="w")

                self.errorfont = font.Font(family="Arial", size=12, weight="bold")
                self.error_label = tk.Label(root, text="", anchor="e", fg="red", font=self.errorfont)
                self.error_label.grid(row=6, columnspan=5, column=0, sticky='w')

                self.make_table()
                self.show_privileged_interface() # Show elements only if logged in (callable from child login form)

        # ----------------------------------------------------
        # Function to update vehicles count display text
        # ----------------------------------------------------
        def check_input(self, *args):

                if len(self.year_entry.get()) > 0:
                        # Make year digits
                        if not self.year_entry.get().isdigit():
                                var = re.sub(r'\D', '', self.year_entry.get())
                                self.year_entry.delete(0, tk.END)  # Clear existing text
                                self.year_entry.insert(0,var[:4]) # Restrict to 4
                                self.year_entry.config(background="white")
                                self.error_label["text"] = ""

                        if len(self.year_entry.get()) > 0:
                                # Make year 4 or less
                                if len(self.year_entry.get()) > 4:
                                        var = self.year_entry.get()
                                        self.year_entry.delete(0, tk.END)  # Clear existing text
                                        self.year_entry.insert(0,var[:4]) # Restrict to 4

                                # Make year pink if this year plus 1
                                if len(self.year_entry.get()) == 4:
                                        current_year = datetime.now().year
                                        if int(self.year_entry.get()) >  current_year + 1:
                                                self.year_entry.config(background="pink")
                                                self.error_label["text"] = "Invalid year"
                                        else:
                                                self.year_entry.config(background="white")
                                                self.error_label["text"] = ""
                                else:
                                        self.year_entry.config(background="pink")
                                        self.error_label["text"] = "Invalid year"
                        else:
                                self.year_entry.config(background="white")
                                self.error_label["text"] = ""
                else:
                        self.year_entry.config(background="white")
                        self.error_label["text"] = ""


        # ----------------------------------------------------
        # Function to update vehicles count display text
        # ----------------------------------------------------
        def update_vehicle_counts(self):
                print("Update vehicle counts")
                self.vehicles_available = nwauto.get_query_results("vehicles_available", {})
                self.vehicles_pending = nwauto.get_query_results("vehicles_pending", {})
                # Handle NULL/EMPTY results!
                avail = 0
                pend = 0
                if len(self.vehicles_pending) > 0:
                        if len(self.vehicles_pending[0]) > 0:
                                pend = self.vehicles_pending[0][0]
                if len(self.vehicles_available) > 0:
                        if len(self.vehicles_available[0]) > 0:
                                avail = self.vehicles_available[0][0]
                print(str(pend),"Pending",str(avail),"Avail")
                self.vehicles_pending_text = "Vehicles Pending Parts: " + str(pend) # Erroneous/extra
                self.vehicles_pending_label["text"] = self.vehicles_pending_text # Actually update UI!
                self.vehicles_available_text = "Vehicles Available: " + str(avail) # Erroneous/extra
                self.vehicles_available_label["text"] = self.vehicles_available_text # Actually update UI!

        # ----------------------------------------------------
        # Function to reload search table and update counts
        # ----------------------------------------------------
        def refresh_search(self):
                self.make_table() # Remake source table with "Privileged user" visibility (columns) - also calls update_vehicle_counts
                self.vehicle_search() # Reload search with "Privileged user" visibility (data)
        # ----------------------------------------------------
        # Function to:
        # 1. display VIN# for privleged user
        # 2. display Report and Sales status drop-down for Manager
        # ----------------------------------------------------
        def show_privileged_interface(self):
                self.refresh_search() 
                # No need to remove these
                if nwauto.is_position("manager") or nwauto.is_position("inventoryclerk") or nwauto.is_position("salesperson"):
                        self.vin_label.grid(row=1, column=0, sticky='w')
                        self.vin_entry.grid(row=1, column=1, sticky='w')
                if nwauto.is_position("manager"):
                        self.salestatus_label.grid(row=1, column=6, sticky='w')
                        self.salestatus_optionmenu.grid(row=1, column=7, sticky='e')
                        #self.report_button.grid(row=5, column=1, sticky='w')
                        self.reports_menu_button.grid(row=5, column=1, sticky='w')
                else:
                        self.salestatus_label.grid_forget()
                        self.salestatus_optionmenu.grid_forget()
                        self.reports_menu_button.grid_forget()
                if nwauto.is_position("manager") or nwauto.is_position("inventoryclerk"):
                        self.vehicles_pending_label.grid(row=5, column=3, sticky='w')
                else:
                        self.vehicles_pending_label.grid_forget()
                if nwauto.is_position("inventoryclerk"):
                        self.addvehicle_button.grid(row=5, column=4, sticky='w')
                else:
                        self.addvehicle_button.grid_forget()

        # ----------------------------------------------------
        # Function to builds the search results table
        # ----------------------------------------------------
        def verifyVIN(self):
                try:
                        self.info_button.config(state="disabled")
                        self.curItem = self.results_tree.focus()
                        #print(self.curItem)
                        if isinstance(self.results_tree.item(self.curItem), dict):
                                if isinstance(self.results_tree.item(self.curItem)["values"], list):
                                        self.curVin = self.results_tree.item(self.curItem)["values"][k_v]
                                        self.info_button.config(state="normal")
                except Error as e:
                        self.curVin = ""
                
        # ----------------------------------------------------
        # Function to builds the search results table
        # ----------------------------------------------------
        def selectItem(self, event):
                self.verifyVIN()
                #print(event, self.results_tree.selection(), self.results_tree.focus())
                #print("VIN#:"+self.results_tree.item(self.curItem)["values"][k_v])
                
        # ----------------------------------------------------
        # Get Vehicle Details
        # ----------------------------------------------------
        def get_vehicle(self):
                self.verifyVIN()
                if self.curVin == "":
                        print("Select a vehicle for info.")
                else:
                        print("Vehicle Info for VIN#: "+self.curVin)
                        # new_dict = {"vin": self.curVin}
                        # get_vehicle = nwauto.get_query_results("get_vehicle", new_dict)
                        self.info_form() # Replace above with this
                        
        # ----------------------------------------------------
        # Buy/Add Vehicle 
        # ----------------------------------------------------
        def add_vehicle(self):
                print("Add vehicle form.")
                self.buy_vehicle_window = tk.Toplevel(self.root)
                self.buy_vehicle_window.transient(self.root)
                self.buy_vehicle_window.grab_set()  # Make child window modal
                x = self.root.winfo_x()
                y = self.root.winfo_y()
                self.buy_vehicle_window.geometry("+%d+%d" %(x+10,y+10))
                buy_vehicle.BuyVehicleForm(self.buy_vehicle_window, "", self)
                
        # ----------------------------------------------------
        # Function to builds the search results table
        # ----------------------------------------------------
        def make_table(self):
                # Selectively show Sale Status, Parts Pending
                # Switch Asking/Sale Price depending on Sale Status
                self.results_tree.destroy()
                self.curVin = ""
                if nwauto.is_position("manager"): 
                        self.vehicle_columns=(c_v, c_vt, c_mn, c_md, c_y, c_f, c_c, c_h, c_ask, c_st, c_pp) # Sales status and parts pending
                elif nwauto.is_position("inventoryclerk"): 
                        self.vehicle_columns=(c_v, c_vt, c_mn, c_md, c_y, c_f, c_c, c_h, c_ask, c_pp) # Parts pending
                else:
                        self.vehicle_columns=(c_v, c_vt, c_mn, c_md, c_y, c_f, c_c, c_h, c_ask) # Public view (incldues salesperson)
                self.results_tree = ttk.Treeview(root, columns=self.vehicle_columns, show="headings", height=20)
                self.results_tree.tag_configure('even', background=nwauto.get_rowcolor("even"))
                self.results_tree.tag_configure('odd', background=nwauto.get_rowcolor("odd"))
                self.results_tree.heading(c_v, text=c_v)
                self.results_tree.heading(c_vt, text=c_vt)
                self.results_tree.heading(c_mn, text=c_mn)
                self.results_tree.heading(c_md, text=c_md)
                self.results_tree.heading(c_y, text=c_y)
                self.results_tree.heading(c_f, text=c_f)
                self.results_tree.heading(c_c, text=c_c)
                self.results_tree.heading(c_h, text=c_h)
                self.results_tree.heading(c_ask, text=c_ask)
                #<<TreeviewSelect>>: Triggered when an item is selected.
                #<<TreeviewOpen>>: Triggered when a node is expanded.
                #<<TreeviewClose>>: Triggered when a node is collapsed.
                #<Double-Button-1>: Triggered when an item is double-clicked.
                #<Button-1>: Triggered when an item is single-clicked.
                #<Button-3>: Triggered when an item is right-clicked.
                self.results_tree.bind('<<TreeviewSelect>>', self.selectItem)
                #self.results_tree.bind('<Button-1>', self.selectItem)
                self.results_tree.column(c_v, width=150)
                self.results_tree.column(c_vt, width=100)
                self.results_tree.column(c_mn, width=100)
                self.results_tree.column(c_md, width=100)
                self.results_tree.column(c_y, width=50)
                self.results_tree.column(c_f, width=70)
                self.results_tree.column(c_c, width=150)
                self.results_tree.column(c_h, width=70)
                self.results_tree.column(c_ask, width=80)
                if nwauto.is_position("manager"):
                        self.results_tree.heading(c_st, text="Status")
                        self.results_tree.column(c_st, width=50)
                if nwauto.is_position("manager") or nwauto.is_position("inventoryclerk"):
                        self.results_tree.heading(c_pp, text="Parts?")
                        self.results_tree.column(c_pp, width=50)
                self.yscrollbar = ttk.Scrollbar(self.root, orient='vertical', command=self.results_tree.yview)
                self.results_tree.configure(yscrollcommand=self.yscrollbar.set)
                self.results_tree.grid(row=3, columnspan=9, sticky="nsew")
                self.yscrollbar.grid(row=3, column=10, sticky='nse')
                self.yscrollbar.configure(command=self.results_tree.yview)
                #self.grid_rowconfigure(0, weight=1)
                #self.grid_columnconfigure(0, weight=1)
                
        # ----------------------------------------------------
        # CR wrapper
        # ----------------------------------------------------
        def vehicle_search_caller(self, event):
                self.vehicle_search()
        # ----------------------------------------------------
        # Function to pass the search input from the search form to the search function
        # ----------------------------------------------------
        def vehicle_search(self):
                self.error_label["text"] = "" # Clear on every refresh
                self.var_dict["vin"] = self.vin_entry.get() # VIN# 
                self.var_dict["keyword"] = self.keyword_entry.get() # Keyword 
                self.var_dict["color"]=self.color_choice.get() # Color
                self.var_dict["vehicle_type"]=self.vehicletype_choice.get() # Vehicle Type
                self.var_dict["fuel_type"]=self.fueltype_choice.get() # Fuel Type
                self.var_dict["manufacturer"]=self.manufacturer_choice.get() # Manufacturer
                self.var_dict["model_year"]=self.year_entry.get().strip() # Manufacturer
                if self.var_dict["model_year"] == "" or not self.var_dict["model_year"].isdigit():
                        self.var_dict["model_year"] = "v.model_year" # Equal to self in SQL
                if nwauto.is_position("manager"):
                        self.var_dict["sale_status"]=self.salestatus_choice.get()
                else:
                        self.var_dict["sale_status"]="All" # Sale Status (UI should be hidden until login - FIX THIS TO BE REAL!)
                nwauto.run_lock("search_vehicle_lock")
                self.update_vehicle_counts() # Always update counts on search re-execution AND after the LOCK
                vehicle_search_results = nwauto.get_query_results("search_vehicle", self.var_dict)
                nwauto.run_unlock() # Unlock tables for search
                print(vehicle_search_results)
                
                for i in self.results_tree.get_children():
                        self.results_tree.delete(i)
                sr = 0 # Rows returned
                public_vehicles_found = 0 # Public rows returned?
                for vehicle in vehicle_search_results:
                        if nwauto.is_position("manager"): 
                                vrow = (vehicle[k_v],vehicle[k_vt],vehicle[k_mn],vehicle[k_md],vehicle[k_y],vehicle[k_f],vehicle[k_c],vehicle[k_h],vehicle[k_ask],vehicle[k_st],vehicle[k_pp])
                                sr = sr + 1
                                self.results_tree.insert("", tk.END, values=vrow, tags=(nwauto.get_tag(sr)))
                        else:
                                if vehicle[k_st] == "Unsold" and (vehicle[k_pp] == "N" or nwauto.is_position("inventoryclerk")):  # Must be unsold and have no parts pending OR unsold and clerk
                                        sr = sr + 1
                                        #vrow = (vehicle[k_v],vehicle[k_vt],vehicle[k_mn],vehicle[k_md],vehicle[k_y],vehicle[k_f],vehicle[k_c],vehicle[k_h],vehicle[k_ask])
                                        if nwauto.is_position("inventoryclerk"): 
                                                vrow = (vehicle[k_v],vehicle[k_vt],vehicle[k_mn],vehicle[k_md],vehicle[k_y],vehicle[k_f],vehicle[k_c],vehicle[k_h],vehicle[k_ask],vehicle[k_pp])
                                        else:
                                                vrow = (vehicle[k_v],vehicle[k_vt],vehicle[k_mn],vehicle[k_md],vehicle[k_y],vehicle[k_f],vehicle[k_c],vehicle[k_h],vehicle[k_ask])
                                        public_vehicles_found += 1
                                        self.results_tree.insert("", tk.END, values=vrow, tags=(nwauto.get_tag(sr)))
                        # c_v, c_vt, c_mn, c_md, c_y, c_f, c_c, c_h, c_ask, ... c_st, c_sld, c_pp
                        #('JA4LS21H22J064586', 'Compact', 'Honda', 'Civic', 2025, 'Hybrid', 'Silver', 141, 'Unsold', None, 35549.99, 'N')
                if public_vehicles_found == 0 and not (nwauto.is_position("manager") or nwauto.is_position("inventoryclerk")):
                        # print("Sorry, it looks like we don’t have that in stock!")
                        # messagebox.showinfo("No Results", "Sorry, it looks like we don’t have that in stock!")
                        self.error_label["text"] = "Sorry, it looks like we don’t have that in stock!"
                elif sr == 0:
                        self.error_label["text"] = "No vehicles found matching search criteria" # Something for privileged user

                print("Vehicles found: " + str(sr))
                # ON EVERY SEARCH: Update the vehicles available (so if you sell or buy a vehicle the summary matches the results queried)
                
        # --------------------------------------------------------------------------------------------------------
        # Populate drop-down source arrays for Vehicle Search form
        # --------------------------------------------------------------------------------------------------------
        def populate_lookups(self):
                # ----------------------------------------------------
                # Vehicle Search Form lookup population
                # ----------------------------------------------------
                self.manufacturers = nwauto.get_query_results("manufacturers", {})
                self.colors = nwauto.get_query_results("colors", {})
                self.vehicle_type = nwauto.get_query_results("vehicle_type", {})
                self.fuel_type = nwauto.get_query_results("fuel_type", {})
                self.sale_status_choice = [('Sold',),('Unsold',)] # All appended automatically
                # ----------------------------------------------------
                # Used elsewhere - testing here
                # ----------------------------------------------------
                self.conditions = nwauto.get_query_results("conditions", {})
        
        #From Brian - Commented out - not sure what this was doing
        #def rebuild_menu_bar(self):
                # self.menu_bar.delete(0, 'end')
                # self.menu_bar.add_cascade(label = "File", menu = self.file_menu)

                # if nwauto.is_position("manager") or nwauto.is_position("owner"):
                #         self.reports_menu = Menu(self.menu_bar, tearoff = 0) 
                #         self.reports_menu.add_command(label = "Sales Report", command = self.open_sales_report)
                #         self.menu_bar.add_cascade(label="Reports", menu=self.reports_menu)
                # else:
                #         self.reports_menu = None
        
        # def open_sales_report(self):
        #         print("Sales Report menu item selected.")

        def make_report(self,sqlfile,title):
                self.child_window = tk.Toplevel(self.root)
                self.child_window.transient(self.root) 
                self.child_window.grab_set() # Make child window modal!
                x = self.root.winfo_x()
                y = self.root.winfo_y()
                self.child_window.geometry("+%d+%d" %(x+10,y+10))
                reports.ReportInfo(self.child_window, sqlfile, title)
        
        def open_seller_history_report(self):
                self.make_report("report_seller_history","Seller History Report")
    
        def open_avg_time_inventory_report(self):
                self.make_report("report_average_time_in_inventory","Average Time in Inventory Report")

        def open_price_per_condition_report(self):
                self.make_report("report_avg_price_per_condition","Price per Condition Report")

        def open_parts_statistics_report(self):
                self.make_report("report_parts_statistics","Parts Statistics Report")

        def open_monthly_sales_report(self):
                self.make_report("report_monthly_sales","Monthly Sales Report")
                
        # --------------------------------------------------------------------------------------------------------
        # Populate drop-downs of Vehicle Search form from object
        # --------------------------------------------------------------------------------------------------------
        def get_dropdown(self, lookup):
                # Dropdown menu options 
                options = [ 
                    "All"
                ]
                for l in lookup:
                        options.append(l[0])
                return options;
                
        # ----------------------------------------------------
        # Function launch the Login Form
        # ----------------------------------------------------
        def login_form(self):
                self.child_window = tk.Toplevel(self.root)
                self.child_window.transient(self.root) 
                self.child_window.grab_set() # Make child window modal!
                x = self.root.winfo_x()
                y = self.root.winfo_y()
                self.child_window.geometry("+%d+%d" %(x+10,y+10))
                login_form.LoginForm(self.child_window, self)
                
        # ----------------------------------------------------
        # Function launch the Vehicle Info Form
        # ----------------------------------------------------
        def info_form(self):
                self.child_window = tk.Toplevel(self.root)
                self.child_window.transient(self.root) 
                self.child_window.grab_set() # Make child window modal!
                x = self.root.winfo_x()
                y = self.root.winfo_y()
                self.child_window.geometry("+%d+%d" %(x+10,y+10))
                info_form.VehicleInfo(self.child_window, self, self.curVin)

try:

        root = tk.Tk()
        root.geometry("1000x550")
        form = vehicle_search_form(root)
        # Start the Tkinter event loop
        root.mainloop()

except Error as e:
    print(e)



