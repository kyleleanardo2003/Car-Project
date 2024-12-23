
import subprocess
import sys
import sqlite3
import json
import os


connection = sqlite3.connect("vehicle.db")
c = connection.cursor()
user_cred = {}
logged_in = False
cur_usr = ""
cred_file = "usr_cred.json"
active = True
DBflag_file = "executed.flag"
auto_file = "executed2.flag"
def load_usr():
    try:
        with open(cred_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error loading cred file\n")
        return{}

def save_cred():
    try:
        with open(cred_file, "w") as file:
            json.dump(user_cred, file)
    except FileNotFoundError:
        print("Error saving file")
        return
def homescreen():
    global active
    global logged_in
    global cur_usr
    usr_input = input("What would you like to do: ")
    if usr_input.lower() == "help":
        help()
    elif usr_input.lower() == "quit":
        if logged_in == False:
            active = False
        else:
            print("Must log out first!")

    elif usr_input.lower() == "login":
        if logged_in == False:
            login()
        else:
            print("Already logged in as " + cur_usr)
    elif usr_input.lower() == "logout":
        if logged_in == True:
            logged_in = False
            cur_usr = ""
            logout()
        else:
            print("Not logged in\n")
    elif usr_input.lower() == "register":
        if logged_in == False:
            register()
        else:
            print("Already logged in\n")
    elif usr_input.lower() == "sort":
        if logged_in:
            sort()
        else:
            print("You must login first!\n")
    elif usr_input.lower() == "backup":
        if logged_in:
            backup()
        else:
            print("You must login first!\n")
    elif usr_input.lower() == "insert":
        if logged_in:
            insert()
        else:
            print("You must login first!\n")
    elif usr_input.lower() == "search":
        if logged_in:
            search()
        else:
            print("You must login first!\n")
    elif usr_input.lower() == "searchfile":
        if logged_in:
            file_name = input("Input which file to search: ")
            search_file(file_name)
        else:
            print("You must login first!\n")
    elif usr_input.lower() == "display":
        if logged_in:
            display()
        else:
            print("You must login first!\n")
    elif usr_input.lower() == "delete":
        if logged_in:
            delete()
        else:
            print("You must login first!\n")
    elif usr_input.lower() == "auto_add":
        if logged_in:
            auto_add()
        else:
            print("You must login first!\n")

    elif usr_input.lower() == "update":
        if logged_in:
            update()
        else:
            print("You must login first!\n")
    else:
        print("Unknown command!\n")

def help():
    print("""
          Auto_add: Automatically adds 5 rows to your database
          Register: Creates a username and password
          Login: Login to the user by providing a username and password
          Logout: Log out of the current user
          Delete: Deletes a vehicle from the database
          Update: Updates vehicle data
          Sort: Sort the database in the desired column/parameters
          Backup: Creates a backup file of database
          Search: Searches for a keyword in the table
          Searchfile (file_name): Searches for a keyword in 'file_name'
          Display: Display the entire table
          Insert: Insert new entry into the table
          """)
def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if username.lower() in user_cred and user_cred[username.lower()] == password:
        global logged_in
        global cur_usr
        logged_in = True
        cur_usr = username
        print("Logged in Successfully\n")
    else:
        print("Invalid password or username\n")
def logout():
    print("\nLoggin out\n")
    global logged_in
    logged_in = False

def register():
    username = input("Enter your desired username: ")
    password = input("Enter your password: ")
    verify_pass = input("Reenter your password: ")
    if verify_pass == password:
        if username.lower() in user_cred:
            print("Username already exists. Please choose a different one")
        else:
            user_cred[username.lower()] = password
            save_cred()
            print("User added successfully.")
    else:
        print("Both passwords must match!")
        register()

def search():
    connection = sqlite3.connect("vehicle.db")
    c = connection.cursor()
    target = input("Enter the keyword to search for: ")
    target_column = input("Enter the column to search in: ")
    query = "SELECT * FROM Vehicle WHERE '%{target_column}%' LIKE '%{target}%'"
    c.execute(query)
    result = c.fetchall()
    for row in result:
        print(row)
    connection.close()

def search_file(file_name):
    target = input("Input target word: ")
    awk_command = "awk '/{word}/ {{print $0}}' {filename}".format(word=target, filename=file_name)
    output = subprocess.check_output(awk_command, shell = True, universal_newlines=True)
    print(output)

def insert():
    id=int(input("Enter the ID Number: "))
    type=input("Enter the Type: ")
    make=input("Enter the Make: ")
    model=input("Enter the Model: ")
    year=input("Enter the Year: ")
    mileage = int(input("Enter the Mileage: "))
    vin = int(input("Enter the VIN: "))
    License_Plate = input("Enter the License_Plate: ")
    c.execute ("INSERT INTO Vehicle (id, type, make, model, year, mileage, vin, License_Plate) VALUES (?,?,?,?,?,?,?,?)", (id, type, make, model, year, mileage, vin, License_Plate) )
    connection.commit()

def display():
    print ()
    sql = "SELECT * from Vehicle"
    for row in connection.execute (sql):
        print(row)
    print ("\n")
def sort():
    sort_type = input("Please enter how you would like the database sorted: ")
    file_path = "./sortdb.pl"
    output = subprocess.run(["perl",  file_path, sort_type], check= True)
    print("\nSorted successfully\n")

def backup():
    file_path = "./cpdatabase"
    subprocess.call(file_path, shell = True)
    print("Successfully created backup")


def update():
    dbID = input ("What is the ID of the Vehicle you want to change? ")
    print ("Data Fields: \n\n     type\n     make\n     model\n     year\n     mileage\n     vin\n     License_Plate\n" )
    type1 = input ("Which data field do you want do change? ")
    type2 = input ("What do you want to change " + type1 + " to? ")

    if type1.lower() == "type":
        sql2 = """UPDATE Vehicle set type = ? WHERE ID = ? ;"""
        val = (type2, dbID)
        c.execute(sql2, val)
        print ("Changed " + type1 + " to " + type2 + " where the ID is " + dbID + "\n")

    elif type1.lower() == "make":
        sql2 = """UPDATE Vehicle set make = ? WHERE ID = ? ;"""
        val = (type2, dbID)
        c.execute(sql2, val)
        print ("Changed " + type1 + " to " + type2 + " where the ID is " + dbID + "\n")

    elif type1.lower() == "model":
        sql2 = """UPDATE Vehicle set model = ? WHERE ID = ? ;"""
        val = (type2, dbID)
        c.execute(sql2, val)
        print ("Changed " + type1 + " to " + type2 + " where the ID is " + dbID + "\n")

    elif type1.lower() == "year":
        type2 = int (input ("Enter year again: "))
        sql2 = """UPDATE Vehicle set year = ? WHERE ID = ? ;"""
        val = (type2, dbID)
        c.execute(sql2, val)
        print ("Changed " + type1 + " to " + str(type2) + " where the ID is " + dbID + "\n")

    elif type1.lower() == "mileage":
        type2 = int (input ("Enter mileage again: "))
        sql2 = """UPDATE Vehicle set mileage = ? WHERE ID = ? ;"""
        val = (type2, dbID)
        c.execute(sql2, val)
        print ("Changed " + type1 + " to " + str(type2) + " where the ID is " + dbID + "\n")

    elif type1.lower() == "vin":
        sql2 = """UPDATE Vehicle set vin = ? WHERE ID = ? ;"""
        val = (type2, dbID)
        c.execute(sql2, val)
        print ("Changed " + type1 + " to " + type2 + " where the ID is " + dbID + "\n")

    elif type1.lower() == "make":
        sql2 = """UPDATE Vehicle set License_Plate = ? WHERE ID = ? ;"""
        val = (type2, dbID)
        c.execute(sql2, val)
        print ("Changed " + type1 + " to " + type2 + " where the ID is " + dbID + "\n")

    else:
        print("Unknown command!\n")


def delete():
    rnum = int(input("What's the ID of the Vehicle you want to delete? "))
    if isinstance(rnum, int):
      sql2 = """DELETE from Vehicle WHERE ID = ? ;"""
      c.execute(sql2, (rnum,))
      print ("Deleted row from Vehicle Database where the Vehicle ID was " + str(rnum))

    else:
      print ("Unknown command:\n")

def auto_add():
    if not os.path.exists(auto_file):
      file_path = "./adddb"
      subprocess.call(file_path, shell = True)
      print("Successfully added vehicles to the database\n")
    else:
      print ("Can only use function Auto_add once")

if __name__ == "__main__":
    os.system('cls||clear')
    print("\n\nWelcome to the Envision-Motors.LLC Vehicle Database")
    print("For a list of functions type HELP\n")
    if not os.path.exists(DBflag_file):
        # Calls the Bash script
        file_path ="./mkdatabase"
        subprocess.call(file_path, shell = True)
        # Create the flag file to indicate that the script has been executed
        with open(DBflag_file, "w"):
            pass
        print("Database created successfully.")
        try:
            with open(cred_file, "w") as file:
                json.dump(user_cred, file)
        except FileNotFoundError:
            print("Error saving file")
    else:
        print("Database has already been created.")
    while active:
        try:
            user_cred = load_usr()
            homescreen()
        except KeyboardInterrupt:
            logout()
            break
