from getpass import getpass
import bcrypt
from secrets import *
import sqlite3
from pprint import pprint


con = sqlite3.connect("userinfo.db")
cur = con.cursor()

#cur.execute("CREATE TABLE TBL_details(id,username,password,email)")

rows = [
        (1, 'aamir', 'qwerty123', 'hzdkv@example.com'),
        (2, 'kaizar', 'pass1', 'asd@example.com'),
        (3, 'ammar', 'something', 'aeh@example.com'),
        (4, 'amin', 'random', 'auwhg@example.com')
]

#cur.executemany("INSERT INTO TBL_details VALUES(?,?,?,?)", rows)
#con.commit()

def user_exist(email):
    user = cur.execute("SELECT * FROM TBL_details WHERE email =?", (email,))
    if user.fetchone() is not None:
        return True
    else:
        return False
    
def code_gen(email):
    if user_exist(email) == False:
        print("user not found")
        exit()
    code = token_urlsafe(32)
    return code
    
def code_checker(email,code,user_inp):#compares the codes to a user inputed code
    if code != user_inp:
        return False
    else:
        return pass_changer(email)
    
def pass_changer(email):
    password = getpass("enter your password")
    while not pass_req(password):
        print("you did not meet req")
        password = getpass("enter your password")
    password = str(hash(password))
    cur.execute("UPDATE TBL_details SET password =? WHERE email =?", (password,email))
    con.commit()
    print("password changed")
    
def hash(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def pass_req(password):# the password requrements(kept it empty for abstraction reasons)
    return True


def get_det():
    cur.execute("SELECT * FROM TBL_details")
    return cur.fetchall()

initial = get_det()


em = 'auwhg@example.com'
code = code_gen(em) # currently manually inputing the code will do an email thing later

u_i = code # need to inject the parameter here from the online form U_i stands for user input

code_checker(em,code,u_i)





final = get_det()


print(initial)
print(final)