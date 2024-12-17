# ----------------------------------------------------
# Team041
# Sailesh Arya, Brian Jiang, Aaron Job Ramirez, Nick vanVeldhuisen
# Python Class info_form.VehicleInfo
# Class purpose: Vehicle Info form
# Depends On: tkinger tk/tkk for forms
#             nwauto.py for MySQL database functions, session variables, etc.
#             sell_vehicle.py for Sell function
#             vehicle_parts_order_form.py for Parts Order form (including Vendor add/search)
# Called By: vehicle_search.py Vehicle Info button
# ----------------------------------------------------

import nwauto
import tkinter as tk
from tkinter import ttk
import sell_vehicle
import vehicle_parts_orders_form

# Not used
#import os
#import sys # To get images
#import base64


class VehicleInfo:
        def __init__(self, master, parent_form, myvin):
                
                self.root = master
                self.root.protocol("WM_DELETE_WINDOW", self.cancel)
                self.parent_form = parent_form
                self.vin = myvin
                self.vehicle_height = 11
                self.root.geometry("500x350")
                if nwauto.is_position("manager") or nwauto.is_position("inventoryclerk"):
                        self.root.geometry("1050x600") 
                        self.vehicle_height = 16
                #self.root.columnconfigure(0, weight=1)
                #self.root.rowconfigure(0, weight=1)
                #errorFont = font.Font(family='Helvetica', name='appHighlightFont', size=10, weight='bold')

                # Lookup for size of part columns and for their order of display
                self.info_partcolumn_dict={"vendor_part_number":100
                                          ,"description":200
                                          ,"vendor_name":150
                                          ,"order_number":160
                                          ,"unit_price":70
                                          ,"quantity":40
                                          ,"status":70}
                                          #,"action":100}

                self.info_partselected_dict={"vendor_part_number":""
                                            ,"vendor_name":""
                                            ,"order_number":""
                                            ,"status":""}

                # Restricted columns (manager sees all)
                self.mgr_cols = ["purchaser_name"
                                ,"salesperson_name"
                                ,"purchase_date"
                                ,"purchase_price"
                                ,"sale_date"
                                ,"part_cost"
                                ,"parts_pending"
                                ,"condition"
                                ,"sale_date"]

                # Subset of restricted columns visible to the inventory clerk
                self.clerk_cols = ["purchase_price"
                                  ,"part_cost"]
                
                # Key decision columns not part of public display but used to pull other data or make decisions
                self.key_columns={"purchaser_name":None
                                 ,"salesperson_name":None
                                 ,"purchase_date":None
                                 ,"purchase_price":None
                                 ,"sale_date":None
                                 ,"part_cost":None
                                 ,"parts_pending":None
                                 ,"seller_type":None
                                 ,"buyer_type":None
                                 ,"buyer":None
                                 ,"seller":None
                                  }
                
                # Vehicle column aliases (public)
                self.col_aliases={"vin":"VIN#"
                                 ,"vehicle_type":"Vehicle Type"
                                 ,"manufacturer":"Manufacturer"
                                 ,"model":"Model"
                                 ,"model_year":"Year"
                                 ,"fuel_type":"Fuel Type"
                                 ,"colors":"Colors"
                                 ,"horsepower":"Horsepower"
                                 ,"sale_price":"Sale Price" 
                                 ,"description":"Description" # Shared by Vehicle and Part in this current solution
                                 ,"purchase_date":"Purchased On" # Constrained
                                 ,"purchase_price":"Purchase Price" # Constrained
                                 ,"sale_date":"Sold On" # Constrained
                                 ,"part_cost":"Parts Cost" # Constrained
                                 ,"parts_pending":"Parts Pending?" # Constrained
                                 ,"condition":"Condition" # Constrained
                                 ,"purchaser_name":"Inventory Clerk" # Constrained
                                 ,"salesperson_name":"Salesperson" # Constrained
                                 # Customer Display (re-used between Buyer/Seller)
                                 ,"individual_name":"Individual Name" 
                                 ,"business_name":"Business Name" 
                                 ,"contact_name":"Contact Name" 
                                 ,"email":"Email" 
                                 ,"phone_number":"Phone Number" 
                                 ,"street_address":"Street Address" 
                                 ,"city":"City" 
                                 ,"state":"State" 
                                 ,"postal_code":"Postal Code" 
                                 ,"order_number":"Order #"
                                 ,"vendor_name":"Vendor"
                                 ,"vendor_part_number":"Part #"
                                 ,"unit_price":"Unit $"
                                 ,"quantity":"Qty"
                                 ,"status":"Status" 
                                 }


                self.info_tree = self.make_table_tree(self.vehicle_height,100,200) # Make so we can destroy/rebuild later stretch=True

                # Verify these are the permissions that allow buyer/seller/parts!
                if nwauto.is_position("manager") or nwauto.is_position("inventoryclerk"):
                        self.buyer_tree = self.make_table_tree(self.vehicle_height,125,150) # Make so we can destroy/rebuild later
                        self.seller_tree = self.make_table_tree(self.vehicle_height,120,150) # Make so we can destroy/rebuild later
                        self.parts_tree = ttk.Treeview(self.root, columns={"Temp":"temp"}, show="headings", height=5) # Make so we can destroy/rebuild later
                

                # Components always shown
                master.title("Vehicle Info Form")
                self.vehicle_label = tk.Label(self.root, text="Vehicle Information")
                self.vehicle_label.grid(row=1, column=0, columnspan=2 )
                self.cancel_button = tk.Button(self.root, text="Close", command=self.cancel)
                self.cancel_button.grid(row=0, column=0, sticky='w')
                self.cancel_button.focus_set() # PUT CURSOR ON CLOSE (CAN CHANGE BASED ON OTHER CONDITIONS LATER)

                # Restricted components (define but don't show)
                self.purchase_label = tk.Label(self.root, text="Purchase Information")
                self.parts_label = tk.Label(self.root, text="Parts Information")
                self.sell_button = tk.Button(self.root, text="Sell", command=self.sell_vehicle)
                self.parts_button = tk.Button(self.root, text="Order Parts", command=self.order_parts)
                self.part_received_button = tk.Button(self.root, text="Part Received", command=self.part_status_received,state="disabled")
                self.part_installed_button = tk.Button(self.root, text="Part Installed", command=self.part_status_installed,state="disabled")

                # Selectively show based on permissions only
                if nwauto.is_position("manager") or nwauto.is_position("inventoryclerk"):
                        self.purchase_label.grid(row=1, column=2, columnspan=2 )
                        self.parts_label.grid(row=4, column=0, columnspan=6 )
                        if nwauto.is_position("inventoryclerk"):
                                self.part_received_button.grid(row=6, column=0)
                                self.part_installed_button.grid(row=6, column=1)
                        
                # Read lookups from database (requires all UI components be defined FIRST)
                try:
                        self.load_grid() 
                except Error as e:
                        print(e)
                        
        # ----------------------------------------------------
        # Close form
        # ----------------------------------------------------
        def cancel(self):
                print("Close")
                self.parent_form.refresh_search() # Update parent form search because parts may be installed or vehicle may be sold!!!
                self.root.destroy()
                self.root.update()

        # ----------------------------------------------------
        # Sell Vehicle
        # ----------------------------------------------------
        def sell_vehicle(self):
                print ("Sell Vehicle Form")
                self.sell_window = tk.Toplevel(self.root)
                self.sell_window.transient(self.root)
                self.sell_window.grab_set() # Make child window modal!
                x = self.root.winfo_x()
                y = self.root.winfo_y()
                self.sell_window.geometry("+%d+%d" %(x+10,y+10))
                sell_vehicle.SellVehicleForm(self.sell_window, self.vin, self)
                
        # ----------------------------------------------------
        # Order Parts
        # ----------------------------------------------------
        def order_parts(self):
                print ("Order Parts Form")
                self.parts_window = tk.Toplevel(self.root)
                self.parts_window.transient(self.root) 
                self.parts_window.grab_set() # Make child window modal!
                x = self.root.winfo_x()
                y = self.root.winfo_y()
                self.parts_window.geometry("+%d+%d" %(x+10,y+10))
                vehicle_parts_orders_form.VehiclePartsForm(self.parts_window, self.vin, self)
                
        # ----------------------------------------------------
        # Set Part Status
        # ----------------------------------------------------
        def part_status(self,status):
                try:
                        print ("Flag vehicle ",self.vin," part ",self.info_partselected_dict," as ",status)
                        nwauto.run_lock("part_lock") # Lock get_vehicle tables
                        new_dict = self.info_partselected_dict
                        new_dict["vin"] = self.vin
                        new_dict["status"] = status
                        # This seems to be a side-effect of an integer in these tables...will be difficult to deal with
                        if isinstance(new_dict["vendor_part_number"], int):
                                new_dict["vendor_part_number"] = str(new_dict["vendor_part_number"]) # Just in case it is a number
                        if isinstance(new_dict["order_number"], int):
                                new_dict["order_number"] = str(new_dict["order_number"]).zfill(3) # Important to maintain leading zero format!
                        nwauto.run_dml("set_vehicle_part_status", new_dict)
                except Error as e:
                        print(e)
                nwauto.run_unlock()
                self.load_grid() 

        # ----------------------------------------------------
        # Set Part Status from buttons
        # ----------------------------------------------------
        def part_status_received(self):
                if self.info_partselected_dict["status"] == "ordered":
                        self.part_status("received")

        def part_status_installed(self):
                if self.info_partselected_dict["status"] == "ordered" or self.info_partselected_dict["status"] == "received":
                        self.part_status("installed")
                
        # ----------------------------------------------------
        # Verify column display based on rules
        # ----------------------------------------------------
        def show_column(self,colname):
                if nwauto.is_position("manager"):
                        return True
                if nwauto.is_position("inventoryclerk") and colname in self.clerk_cols:
                        return True
                if colname not in self.mgr_cols:
                        return True
                return False
        
        # ----------------------------------------------------
        # Property/Value Table
        # ----------------------------------------------------
        def make_table_tree(self,myheight,col1w, col2w):
                thesecolumns=("Property","Value")
                thistree = ttk.Treeview(self.root, columns=thesecolumns, show="headings", height=myheight) # Make Configurable?
                # verscrlbar = ttk.Scrollbar(self.root, orient ="vertical", command = thistree.yview) # Fix this?
                #self.verscrlbar.pack(side ='right', fill ='x')
                thistree.tag_configure('even', background=nwauto.get_rowcolor("even"))
                thistree.tag_configure('odd', background=nwauto.get_rowcolor("odd"))
                thistree.column(0, width=col1w, stretch=True) # Make Configurable?
                thistree.column(1, width=col2w, stretch=True) # Make Configurable?
                thistree.heading(0, text="Property") # Make Configurable?
                thistree.heading(1, text="Value") # Make Configurable?
                verscrlbar = ttk.Scrollbar(self.root,orient ="vertical", command = thistree.yview)
                return thistree
        
        # ----------------------------------------------------
        # Get Vehicle Details On Startup
        # ----------------------------------------------------
        def load_grid(self):
                try:
                        print(self.vin)
                        # Remake Table
                        self.info_tree.destroy()
                        self.info_tree = self.make_table_tree(self.vehicle_height,100,350)
                        self.info_tree.grid(row=3, column=0, columnspan=2, sticky="w") 
                        # self.hscrollbar = ttk.Scrollbar(self.root,orient=tk.HORIZONTAL,command=self.info_tree.xview)
                        # self.info_tree.configure(xscrollcommand=self.hscrollbar.set)
                        # self.vscrollbar = ttk.Scrollbar(self.root,orient=tk.VERTICAL,command=self.info_tree.yview)
                        # self.info_tree.configure(yscrollcommand=self.vscrollbar.set)
                        # self.vscrollbar.grid(row=3, column=2, sticky='nse')
                        # self.hscrollbar.grid(row=4, column=0, columnspan=2, sticky='wse')
                        # Get Data WITH COLUMN METADATA
                        new_dict = {"vin": self.vin}
                        nwauto.run_lock("get_vehicle_lock") # Lock get_vehicle tables
                        get_vehicle, cols = nwauto.get_query_results_with_columns("get_vehicle", new_dict)
                        salesperson = ()
                        inventoryclerk = ()
                        # Put Vehicle Data In Table for first row
                        sr = 0 # Data shown (for even/odd coloring)
                        for row in get_vehicle:
                                r = 0 # R is actually column but there should be only one row here
                                for col in cols:
                                        if col in self.key_columns.keys():
                                                self.key_columns[col] =  row[r] 
                                                print("Key Decision Column:",col,row[r])
                                        if col in self.col_aliases: # What we choose to show as output
                                                if col == "salesperson_name":
                                                        salesperson = (self.col_aliases[col],row[r]) # Save to show with buyer info if sold (otherwise shows a blank)
                                                elif col == "purchaser_name":
                                                        inventoryclerk = (self.col_aliases[col],row[r]) # Save to show with seller info
                                                elif self.show_column(col):
                                                        vrow = (self.col_aliases[col],nwauto.wrap_text(row[r],70)) # Not working well
                                                        sr = sr + 1
                                                        if col == "description":
                                                                self.info_tree.insert("", tk.END, values=vrow, tags=(nwauto.get_tag(sr))) # Here is where we could do something different
                                                        else:
                                                                self.info_tree.insert("", tk.END, values=vrow, tags=(nwauto.get_tag(sr)))
                                        r = r + 1
                        # Show customer data (Seller and, if applicable, Buyer) for the Manager
                        if nwauto.is_position("manager"): # !!! LOTS OF OPPORTUNITY FOR CODE IMPROVEMENT HERE FOR SHARED FUNCTION !!! -NvV
                                print("Show Customer data")
                                # Seller of car to us
                                if not (self.key_columns["seller"] is None or self.key_columns["seller_type"] is None): # Trust issues with database in this conditional...
                                        s_dict = {"customer_id": str(self.key_columns["seller"])} # Current SQL replacement logic expects strings, not numbers
                                        if  self.key_columns["seller_type"] == 'Individual':
                                                sqlfile = "get_vehicle_customer_individual"
                                        if  self.key_columns["seller_type"] == 'Business': # No checks/handling for neither
                                                sqlfile = "get_vehicle_customer_business"
                                        get_seller, scols = nwauto.get_query_results_with_columns(sqlfile, s_dict)
                                        print(get_seller,scols)
                                        self.seller_tree.destroy()
                                        self.seller_tree = self.make_table_tree(self.vehicle_height,120,150)
                                        self.seller_tree.grid(row=3, column=2, columnspan=2, sticky='w')
                                        # Insert first row as inventory clerk who bought the car 
                                        sr = 1
                                        self.seller_tree.insert("", tk.END, values=inventoryclerk, tags=(nwauto.get_tag(sr)))
                                        for row in get_seller:
                                                r = 0 # R is actually column but there should be only one row here
                                                for col in scols:
                                                        if col in self.col_aliases.keys(): # What we choose to show as output
                                                                vrow = ("Seller " + self.col_aliases[col],row[r])
                                                                if self.show_column(col):
                                                                        sr = sr + 1
                                                                        self.seller_tree.insert("", tk.END, values=vrow, tags=(nwauto.get_tag(sr)))
                                                        r = r + 1
                                # Buyer of car if sold
                                if not (self.key_columns["sale_date"] is None or self.key_columns["buyer"] is None or self.key_columns["buyer_type"] is None): # Trust issues with database in this conditional...
                                        b_dict = {"customer_id": str(self.key_columns["buyer"])} # Current SQL replacement logic expects strings, not numbers
                                        if  self.key_columns["buyer_type"] == 'Individual':
                                                sqlfile = "get_vehicle_customer_individual"
                                        if  self.key_columns["buyer_type"] == 'Business': # No checks/handling for neither
                                                sqlfile = "get_vehicle_customer_business"
                                        get_buyer, bcols = nwauto.get_query_results_with_columns(sqlfile, b_dict)
                                        print(get_buyer,bcols)
                                        self.buyer_label = tk.Label(self.root, text="Sales Information")
                                        self.buyer_label.grid(row=1, column=4, columnspan=2 )
                                        self.buyer_tree.destroy()
                                        self.buyer_tree = self.make_table_tree(self.vehicle_height,125,150)
                                        self.buyer_tree.grid(row=3, column=4, columnspan=2, sticky='w')
                                        sr = 1
                                        self.buyer_tree.insert("", tk.END, values=salesperson, tags=(nwauto.get_tag(sr)))
                                        for row in get_buyer:
                                                r = 0 # R is actually column but there should be only one row here
                                                for col in bcols:
                                                        if col in self.col_aliases.keys(): # What we choose to show as output
                                                                vrow = ("Buyer " + self.col_aliases[col],row[r])
                                                                if self.show_column(col):
                                                                        sr = sr + 1
                                                                        self.buyer_tree.insert("", tk.END, values=vrow, tags=(nwauto.get_tag(sr)))
                                                        r = r + 1

                        if (nwauto.is_position("inventoryclerk") or nwauto.is_position("manager")):
                                print("Show All Parts Orders/Parts")
                                self.buildPartTable()

                        # Show Buttons based on permissions AND DATA STATUS WHICH CAN CHANGE!
                        if self.key_columns["sale_date"] is None and self.key_columns["parts_pending"] == "N" and nwauto.is_position("salesperson"):
                                # Show sell button
                                print("Show Sell button if salesperson permissions, car is unsold, and car has no parts pending")
                                self.sell_button.grid(row=0, column=1, sticky='w')
                        else:
                                if self.sell_button.winfo_ismapped():
                                        self.sell_button.grid_remove()

                        # Show Buttons based on permissions AND DATA STATUS WHICH CAN CHANGE!
                        if self.key_columns["sale_date"] is None and nwauto.is_position("inventoryclerk"):
                                # Show add parts order button
                                print("Show Add Parts Order button if unsold and inventoryclerk permissions")
                                self.parts_button.grid(row=0, column=2, sticky='w')
                        else:
                                if self.parts_button.winfo_ismapped():
                                        self.parts_button.grid_remove()

                except Error as e:
                        print(e) # Important to catch errors so unlock table runs

                nwauto.run_unlock() # Unlock tables

        # ----------------------------------------------------
        # Function to check the selected part and enable/disable part action buttons
        # ----------------------------------------------------
        def buildPartTable(self):
                # Create part column tuple of aliased names for display
                partcols = ()
                for col in self.info_partcolumn_dict.keys():
                        if col in self.col_aliases.keys():
                                partcols = (*partcols,self.col_aliases[col]) # Heading created in desired order from base column name

                # Create treeview of data for parts
                self.parts_tree.destroy()
                self.parts_tree = ttk.Treeview(self.root, columns=partcols, show="headings", height=5) # Match this I guess
                self.parts_verscrlbar = ttk.Scrollbar(self.root,orient ="vertical", command = self.parts_tree.yview)
                self.parts_tree.bind('<<TreeviewSelect>>', self.selectPart)
                self.parts_tree.tag_configure('even', background=nwauto.get_rowcolor("even"))
                self.parts_tree.tag_configure('odd', background=nwauto.get_rowcolor("odd"))
                # Set part heading sizes and aliased headings
                colnum = 0
                for ptcol in self.info_partcolumn_dict.keys():
                        self.parts_tree.column(colnum, width=self.info_partcolumn_dict[ptcol])
                        self.parts_tree.heading(colnum, text=self.col_aliases[ptcol])
                        colnum = colnum + 1
                self.parts_tree.grid(row=5, column=0, columnspan=6, sticky="w")

                get_parts, pcols = nwauto.get_query_results_with_columns("get_vehicle_parts", {"vin": self.vin}) # Get vehicle parts with vin #
                print(get_parts,pcols)
                sr = 0
                for row in get_parts:
                        vrow=()
                        for col in self.info_partcolumn_dict.keys():
                                r = 0 # R is actually the column # :-)
                                for pcol in pcols:
                                        if pcol == col and pcol in self.col_aliases.keys(): # Column found for order and has an alias
                                                vrow=(*vrow,row[r])
                                                # if (col == "status" and self.key_columns["sale_date"] is None and nwauto.is_position("inventoryclerk")):
                                                #         if (row[r] == "ordered"):
                                                #                 vrow=(*vrow,"Inst/Rcv") # action after status
                                                #         if (row[r] == "received"):
                                                #                 vrow=(*vrow,"Inst") # action after status
                                        r = r + 1
                        sr = sr + 1
                        self.parts_tree.insert("", tk.END, values=vrow, tags=(nwauto.get_tag(sr)))


        # ----------------------------------------------------
        # Function to check the selected part and enable/disable part action buttons
        # ----------------------------------------------------
        def checkPart(self):
                try:
                        self.part_received_button.config(state="disabled")
                        self.part_installed_button.config(state="disabled")
                        if nwauto.is_position("inventoryclerk"):
                                self.curItem = self.parts_tree.focus()
                                if isinstance(self.parts_tree.item(self.curItem), dict): # If the parts tree item is dictionary
                                        if isinstance(self.parts_tree.item(self.curItem)["values"], list): # If the parts tree item values is a list
                                                # Find / save key part values to use
                                                i = 0
                                                for col in self.parts_tree["columns"]: # For each part column heading
                                                        for partkey in self.info_partselected_dict.keys(): # For each part key column
                                                                if self.col_aliases[partkey] == col: # Current column alias is for a part key
                                                                        self.info_partselected_dict[partkey] = self.parts_tree.item(self.curItem)["values"][i]  # Persist this slected part key
                                                        i = i + 1 
                                                print(self.info_partselected_dict)
                                                statusvalue = self.info_partselected_dict["status"] 
                                                if statusvalue == "ordered":
                                                        self.part_received_button.config(state="normal")
                                                        self.part_installed_button.config(state="normal")
                                                if statusvalue == "received":
                                                        self.part_installed_button.config(state="normal")
                except Error as e:
                        print(e)
                
        # ----------------------------------------------------
        # Function that executes an event (not checked) on selection of the row
        # ----------------------------------------------------
        def selectPart(self, event):
                self.checkPart()
