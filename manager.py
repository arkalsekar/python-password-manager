from getpass import getpass
import os 
import mysql.connector
import argparse
from mysql.connector import errors
import random

print("INFO - Trying to Connect to the DB. ")
mydb = mysql.connector.connect(
host="localhost",
user='root',
password='root',
database="passmanager")

print("INFO - Setting the Database")
mycursor = mydb.cursor()
print("INFO - Connected to the DB. ")

def random_id():
    a = random.randint(100, 999)
    sql = "SELECT id from passmanger"
    mycursor.execute(sql)
    result = mycursor.fetchall()

    for i in result:
        if a in i:
            b = random.randint(1000, 2000)
            return b
    return a

# Taking Arguments for the DB
parser = argparse.ArgumentParser(description = "A Simple Password manager")

parser.add_argument("-u", "--uname", type = str, default = None, required=False,
                        help = "Username")
parser.add_argument("-e", "--email", type = str, default = "arkalsekar10@gmail.com",
                        help = "Email")
parser.add_argument("-p", "--passw", type = str, default = None, required=False,
                        help = "Password")
parser.add_argument("-s", "--site", type = str, default ="arkalsekar.com", required=False,
                        help = "site")
parser.add_argument("-a", "--all", type = str, default = None, required=False,
                        help = "Get All the Data in the DB")
parser.add_argument("-q", "--query", type = str, default = None, required=False,
                        help = "Query Specific Data from the DB")
parser.add_argument("-d", "--delete", type = str, default = None, required=False,
                        help = "Delete Specific Data from the DB via Site Name")
     
args = parser.parse_args()



# Getting No of Values in DB
sql = "SELECT * from passmanger"
mycursor.execute(sql)
my_result = mycursor.fetchall()
len_db = random_id()

# INSERT THE VALUE
if args.uname is not None and args.passw is not None:
    sql = "INSERT INTO passmanger (id, username, email, password, site) VALUES (%s, %s, %s, %s, %s)"
    val = (len_db, args.uname, args.email, args.passw, args.site)
    mycursor.execute(sql, val)
    mydb.commit()
    print("INFO -", mycursor.rowcount, "record inserted.")

# Display all the Data
if args.all is not None:
    for i in my_result:
        print(i)

# Display Specific Data 
if args.query is not None and len(args.query) > 3:
    sql = str(args.query)
    # print(sql)
    try:
        mycursor.execute(sql)
        result = mycursor.fetchall()
        for i in result:
            print(i)
    except errors.ProgrammingError as e:
        print("ERROR -" , e)

# Delete Data via its site name
if args.delete is not None and len(args.delete) > 3:
    sql = str(f"DELETE FROM passmanger WHERE site='{args.delete}'")
    print(sql)
    # print(sql)
    try:
        mycursor.execute(sql)
        mydb.commit()
        print(f'INFO - Deletion for {args.delete} is Sucessful')
    except errors.ProgrammingError as e:
        print("ERROR -" , e)

