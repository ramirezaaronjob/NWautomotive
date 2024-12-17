# --------------------------------------------------------------------------------------------------------
# Team041
# Sailesh Arya, Brian Jiang, Aaron Job Ramirez, Nick vanVeldhuisen
# Abstract Code SQL Checks in Python
# Script purpose: Walkthrough AC in target language
# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
# NOTE: The project 2 AC/SQL syntax of $var for variables was useful for a different language
#       than python, which uses {varname} or %varname. So what we must do is run string replacements on
#       our SQL using variable dictionaries looking for $varname (which is not natural in SQL so works.)
# --------------------------------------------------------------------------------------------------------

import mysql.connector
from mysql.connector import connect, Error
import sys
import os
import tkinter as tk

# ----------------------------------------------------
# GLOBAL APPLICATION SETTINGS/VARIABLES
# ----------------------------------------------------
debug = 1

# ----------------------------------------------------
# SQL file path as subdirectory relative to here
# Default MySQL port is 3306
# Aaron had it on 3307
# if we must support both, this block must be in a
# routine that takes the TCP/IP port and we must
# call it on startup
# ----------------------------------------------------
try:
    connection = connect(
            host="localhost",
            user="gatechUser",
            password="gatech123",
            database="cs6400_fa17_team041",
            #port=3307
            )
    
except Error as e:
    print(e)

# ----------------------------------------------------
# SQL file path as subdirectory relative to here
# ----------------------------------------------------
file_path = os.path.dirname(sys.argv[0]) # os.path.realpath(__file__)
sql_path = os.path.join(file_path,'SQL')

# ----------------------------------------------------
# Desktop application is the session, so globals are session vars until login
# ----------------------------------------------------
session_dict = {
      "inventoryclerk" : False
    , "manager" : False
    , "salesperson" : False
    , "username" : ""}

# --------------------------------------------------------------------------------------------------------
# Get SQL from file in relative path above, removing carriage returns and the ending semicolon
# (does NOT handle commments! So there can be no inline comments in SQL with this.)
# --------------------------------------------------------------------------------------------------------
def get_sql(sql_file):
    file = open(os.path.join(sql_path,sql_file), 'r')
    out_string = file.read().replace(';','').replace('\n',' ')
    file.close()
    return out_string
    
# --------------------------------------------------------------------------------------------------------
# Set variables into SQL string from dictionary
# --------------------------------------------------------------------------------------------------------
def set_vars(sql_string, variabledict):
    # ----------------------------------------------------
    # Use dictionary for variable substitution in SQL
    # ----------------------------------------------------
    out_string = sql_string
    if debug > 0:
        print("==============")
        print("SQL WITH VARIABLES --> " + out_string)
        print("--------------")
        print("VARIABLE DICTIONARY")
        print(variabledict)
        print("--------------")
    for key in variabledict.keys():
        out_string = out_string.replace("$"+key,variabledict[key].replace("'","''"))
    if debug > 0:
        print("SQL WITH VALUES --> " + out_string)
        print("==============")
    return out_string
          
# --------------------------------------------------------------------------------------------------------
# Execute SQL that returns data (rows) in an array and columns names in a 2nd array
# --------------------------------------------------------------------------------------------------------
def get_query_results(queryfile, variabledict):

    records = []
    try:
        query = get_sql(queryfile+".sql") 
        myquery = set_vars(query, variabledict)
        with connection.cursor() as cursor:
             cursor.execute(myquery)
             result = cursor.fetchall()
             for row in result:           
                 records.append(row)
    except Error as e:
        print(e)
    return records

# --------------------------------------------------------------------------------------------------------
# Execute SQL that returns data (rows) in an array and columns names in a 2nd array
# --------------------------------------------------------------------------------------------------------
def get_query_results_with_columns(queryfile, variabledict):

    records = []
    field_names = []
    try:
        query = get_sql(queryfile+".sql") 
        myquery = set_vars(query, variabledict)
        with connection.cursor() as cursor:
             cursor.execute(myquery)
             field_names = [i[0] for i in cursor.description]
             if debug > 0:
                 print("--------------")
                 print("COLUMNS:")
                 print(field_names)
                 print("--------------")
             result = cursor.fetchall()
             for row in result:           
                 records.append(row)
    except Error as e:
        print(e)
    return records, field_names
        
# --------------------------------------------------------------------------------------------------------
# Execute SQL that changes data
# --------------------------------------------------------------------------------------------------------
def run_dml(dml_sql, variabledict):
    dml_result = 0
    try:
        dml_query = get_sql(dml_sql + ".sql")
        my_dml = set_vars(dml_query, variabledict)
        cursor = connection.cursor()
        cursor.execute(my_dml)
        if cursor.lastrowid > 0: # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-lastrowid.html
             dml_result = cursor.lastrowid
             print("Returning dml_result:",dml_result)
        connection.commit()
        if debug > 0:
            print("--------------")
            print("DML RESULTS")
            print("--------------")
            print(cursor.rowcount, "record(s) affected")
            if dml_result > 0:
                 print(str(dml_result),"Last row ID")
    except Error as e:
        print(e)
        dml_result = -1
    
    return(dml_result)

        
# cursor.execute("START TRANSACTION")
# connection.commit()
# connection.rollback()

# --------------------------------------------------------------------------------------------------------
# Execute SQL that locks data
# --------------------------------------------------------------------------------------------------------
def run_lock(lock_sql):
    try:
        cursor = connection.cursor()
        my_lock = get_sql(lock_sql+".sql")
        cursor.execute(my_lock)
        if debug > 0:
            print("--------------")
            print("RAN THIS LOCK")
            print("--------------")
            print(my_lock)
    except Error as e:
        print(e)
    
# --------------------------------------------------------------------------------------------------------
# Execute SQL that unlocks data
# --------------------------------------------------------------------------------------------------------
def run_unlock():
    try:
        cursor = connection.cursor()
        cursor.execute("UNLOCK TABLES")
        if debug > 0:
            print("--------------")
            print("RAN UNLOCK TABLES")
            print("--------------")
    except Error as e:
        print(e)

# ----------------------------------------------------
# Global function to get username for buy/sell vehicle
# ----------------------------------------------------
def get_username():
    return session_dict["username"]

# ----------------------------------------------------
# Global function to check position boolean variable
# ----------------------------------------------------
def is_position(pos):
    pos_return = False
    if pos in session_dict:
        pos_return = session_dict[pos] # Could check for boolean here...
    else:
        print("ERROR: Request for ",pos," which is not defined!")
    return pos_return

# ----------------------------------------------------
# Global function to set session position boolean variables
# ----------------------------------------------------
def login(username, password):
    login_return = False
    try:
        # Clear it before setting it (logging in attempt effectively logs out - maybe hide Login, show Logout?)
        session_dict["inventoryclerk"] = False
        session_dict["manager"] = False
        session_dict["salesperson"] = False
        session_dict["username"] = ""
        #print(session_dict)

        # Query database
        var_dict = { "Username" : username, "Password" : password }
        login_results = get_query_results("get_employee_position", var_dict)
        print(login_results)
        
        # Set session_dict vars
        for row in login_results:
            #print("Applying position permission:",row[0])
            session_dict[row[0]]=True # Each position is a boolean
            login_return = True # Run multiple times for owner
            session_dict["username"] = username # Run multiple times for owner
        #print(session_dict)
            
    except Error as e:
        print(e)
    return login_return

# ----------------------------------------------------
# Even Odd
# ----------------------------------------------------
def get_tag(evenoddnum):
        if evenoddnum % 2 == 0:
                return "even"
        else:
                return "odd"

# ----------------------------------------------------
# Get Color
# ----------------------------------------------------
def get_rowcolor(evenodd):
        if evenodd == "even":
                return "white"
        else:
                return "#E9FEFF"

# ----------------------------------------------------
# Wrap text routine (doesn't really help with tkinter)
# ----------------------------------------------------
def wrap_text(text, width):
    if text is None: # Just in case
         return None
    if not isinstance(text, str): # For ALL inputs tried here
         return text

    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= width:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "

    if current_line:
        lines.append(current_line.strip())

    return "\n".join(lines)
