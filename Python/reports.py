# ----------------------------------------------------
# Team041
# Sailesh Arya, Brian Jiang, Aaron Job Ramirez, Nick vanVeldhuisen
# Script purpose: Vehicle reporting
# Called By: Main program startup 
# ----------------------------------------------------

import nwauto
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re


# selectedyearmonth = "" # Global because not a class

# # GENERIC show_report
# def show_report(root, report_sql, report_title):
     
class ReportInfo:
    def __init__(self, master, report_sql, report_title):

        try:
            self.root = master
            self.root.protocol("WM_DELETE_WINDOW", self.close_report)


            # self.parent_form = parent_form
            self.selectedyearmonth = "" # Global because not a class
            nwauto.run_lock(report_sql+"_lock") # Lock (report specific)
            self.reportData, self.report_cols = nwauto.get_query_results_with_columns(report_sql, {}) # Run starting report (no argumnts)
            nwauto.run_unlock() # Unlock
            print(self.report_cols) # Already aliased in SQL!
            print(self.reportData)

            # Create new window for report
            # self.report_window = tk.Toplevel(root)
            # root.protocol("WM_DELETE_WINDOW", close_report)
            self.root.title(report_title) # "Average Time in Inventory Report")

            # Define columns for new window
            # columns = ("Vehicle Type", "Vehicles Sold", "Average Days in Inventory")

            self.tree = ttk.Treeview(self.root, columns = self.report_cols, show = 'headings', selectmode ='browse')
            #self.tree.pack(fill = tk.BOTH, expand = True, side = 'right')
            self.tree.grid(row=0, column=0, sticky="nsew")
            self.scrollbar_y = ttk.Scrollbar(self.root, orient='vertical', command=self.tree.yview)
            #self.scrollbar_y.pack(side='right', fill='y')
            self.scrollbar_y.grid(row=0, column=1, sticky="nse")
            self.tree.configure(yscrollcommand=self.scrollbar_y.set)

            i = 0
            count_col = -1
            cost_col = -1
            for col in self.report_cols:
                self.tree.heading(i, text=col)
                if report_sql == 'report_seller_history':
                    if col == 'Average Parts Count':
                        count_col = i
                    if col == 'Average Parts Cost':
                        cost_col = i
                i = i + 1

            self.tree.tag_configure('oddRow', background=nwauto.get_rowcolor("odd")) # 'white'
            self.tree.tag_configure('evenRow', background=nwauto.get_rowcolor("even")) #  '#E9FEFF'
            self.tree.tag_configure('redRow', background = 'red')

            i = 0
            for row in self.reportData:
                tag = 'evenRow' if i % 2 == 0 else 'oddRow'
                if report_sql == 'report_seller_history':
                    print('Check',row)
                    if count_col > -1 and cost_col > -1: # Check for column detection
                        if row[count_col] is not None and self.get_monetary_value(row[cost_col])  is not None : # Check for nulls
                            if row[count_col] >= 5 or self.get_monetary_value(row[cost_col])  >= 500:
                                tag = 'redRow'
                i = i + 1
                self.tree.insert("", tk.END, values=row, tags=(tag,))



            self.cancel_button = tk.Button(self.root, text="Close", command=self.close_report)
            #self.cancel_button.pack(side='bottom')
            self.cancel_button.grid(row=1, column=0, sticky="w")

            if report_sql == "report_monthly_sales":
                self.tree.bind('<<TreeviewSelect>>', self.selectMonth)
                self.monthdetail_button = tk.Button(self.root, text="Detail", command=self.show_monthdetail_report)
                #self.monthdetail_button.pack()
                self.monthdetail_button.grid(row=1, column=0, sticky="e")
                self.monthdetail_button.config(state="disabled")

        except Error as e:
            messagebox.showerror("Error: Cannot run report:", str(e))

        nwauto.run_unlock() # Unlock again at end just in case there is error

    def get_monetary_value(self,string):
        match = re.search(r'[\d,.]+', string)
        if match:
            return float(match.group().replace(',', ''))
        else:
            return None
    # ----------------------------------------------------
    # Function that closes main report window
    # ----------------------------------------------------
    def close_report(self):
        try:
            print("Close report")
            self.root.destroy()
            self.root.update()

        except Error as e:
            messagebox.showerror("Error: Close report error:", str(e))

    # ----------------------------------------------------
    # Function that executes an event on selection of monthly sales report row
    # ----------------------------------------------------
    def selectMonth(self,event):
            # Global because not a class
            self.selectedyearmonth = "" # Global because not a class
            self.curItem = self.tree.focus()
            if isinstance(self.tree.item(self.curItem), dict): # If the parts tree item is dictionary
                    if isinstance(self.tree.item(self.curItem)["values"], list): # If the parts tree item values is a list
                            # Find / save key part values to use
                            i = 0
                            for col in self.tree["columns"]: # For each part column heading
                                if col == "Year/Month":
                                    self.selectedyearmonth  = self.tree.item(self.curItem)["values"][i]
                                    print("Selected Month",self.selectedyearmonth)
                                    self.monthdetail_button.config(state="normal")
                                i = i + 1 

    # Month detail report
    def show_monthdetail_report(self):
        try:
            nwauto.run_lock("report_month_sales_detail_lock") # Lock (report specific)
            reportDetailData, report_detail_cols = nwauto.get_query_results_with_columns("report_month_sales_detail", {"yearmonth":str(self.selectedyearmonth)}) # Run starting report (no argumnts)
            nwauto.run_unlock() # Unlock
            print(report_detail_cols) 
            print(reportDetailData)

            # Create new window for report
            self.report_detail_window = tk.Toplevel(self.root)
            self.report_detail_window.protocol("WM_DELETE_WINDOW", self.close_detail_report)
            x = self.root.winfo_x()
            y = self.root.winfo_y()
            self.report_detail_window.geometry("+%d+%d" %(x+10,y+10))
            self.report_detail_window.title(f"Monthly Sales Report Detail {self.selectedyearmonth}") 

            # Define columns for new window
            # columns = ("Vehicle Type", "Vehicles Sold", "Average Days in Inventory")

            detailtree = ttk.Treeview(self.report_detail_window, columns = report_detail_cols, show = 'headings', selectmode ='browse')
            #detailtree.pack(fill = tk.BOTH, expand = True, side = 'right')
            detailtree.grid(row=0, column=0, sticky="nsew")
            scrollbar_y = ttk.Scrollbar(self.report_detail_window, orient='vertical', command=detailtree.yview)
            #self.scrollbar_y.pack(side='right', fill='y')
            scrollbar_y.grid(row=0, column=1, sticky="nse")
            detailtree.configure(yscrollcommand=scrollbar_y.set)

            i = 0
            for col in report_detail_cols:
                detailtree.heading(i, text=col)
                i = i + 1

            detailtree.tag_configure('oddRow', background=nwauto.get_rowcolor("odd")) # 'white'
            detailtree.tag_configure('evenRow', background=nwauto.get_rowcolor("even")) #  '#E9FEFF'
            detailtree.tag_configure('redRow', background = 'red')

            i = 0
            for row in reportDetailData:
                tag = 'evenRow' if i % 2 == 0 else 'oddRow'
                i = i + 1
                detailtree.insert("", tk.END, values=row, tags=(tag,))


        except Error as e:
            messagebox.showerror("Error: Cannot run detail report:", str(e))

        nwauto.run_unlock() # Unlock again at end just in case there is error

    # ----------------------------------------------------
    # Function that closes main report window
    # ----------------------------------------------------
    def close_detail_report(self):
        try:
            print("Close detail report")
            self.report_detail_window.destroy()
            self.report_detail_window.update()

        except Error as e:
            messagebox.showerror("Error: Close detail report error:", str(e))

# def show_seller_history_report(root, connection):
#     report_window = tk.Toplevel(root)
#     report_window.title("Seller History Report")

#     # Define columns for new window
#     columns = ("Seller Name", "Total Vehicles Sold", "Average Purchase Price", "Average Parts Count", "Average Parts Cost")

#     tree = ttk.Treeview(report_window, columns = columns, show = 'headings')
#     tree.pack(fill = tk.BOTH, expand = True)

#     for col in columns:
#         tree.heading(col, text=col)

#     tree.tag_configure('oddRow', background='white')
#     tree.tag_configure('evenRow', background= '#E9FEFF')
#     tree.tag_configure('redRow', background = 'red')
#     reportData = SellerHistory(connection)

#     for i, row in reportData.iterrows():
#         if row['Average Parts Count'] >= 5 or row['Average Parts Cost'] >= 500:
#             tag = 'redRow'
#         else:
#             tag = 'evenRow' if i % 2 == 0 else 'oddRow'
#         tree.insert("", tk.END, values=(row["Seller Name"], row["Total Vehicles Sold"], row["Average Purchase Price"], row["Average Parts Count"], row["Average Parts Cost"]), tags=(tag,))

#     scrollbar_y = ttk.Scrollbar(report_window, orient='vertical', command=tree.yview)
#     scrollbar_y.pack(side='right', fill='y')
#     tree.configure(yscrollcommand=scrollbar_y.set)


# def show_monthly_sales_report(root, connection):
#     report_window = tk.Toplevel(root)
#     report_window.title("Monthly Sales Report")

#     # Define columns for new window
#     columns = ("Year/Month", "Vehicles Sold", "Gross Income", "Net Income")

#     tree = ttk.Treeview(report_window, columns = columns, show = 'headings')
#     tree.pack(fill = tk.BOTH, expand = True)

#     for col in columns:
#         tree.heading(col, text=col)

#     tree.tag_configure('oddRow', background='white')
#     tree.tag_configure('evenRow', background= '#E9FEFF')

#     reportData = monthlySales(connection)

#     for i, row in reportData.iterrows():
#         tag = 'evenRow' if i % 2 == 0 else 'oddRow'
#         tree.insert("", tk.END, values=(row["Year/Month"], row["Vehicles Sold"], row["Gross Income"], row["Net Income"]), tags=(tag,))

#     scrollbar_y = ttk.Scrollbar(report_window, orient='vertical', command=tree.yview)
#     scrollbar_y.pack(side='right', fill='y')
#     tree.configure(yscrollcommand=scrollbar_y.set)

