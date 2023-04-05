from getpass import getpass
import bcrypt
from secrets import *
import sqlite3
from pprint import pprint


con = sqlite3.connect("userinfo.db")
cur = con.cursor()

#cur.execute("CREATE TABLE det(id,username,password,email)")

"""
        (1, 'aamir', 'qwerty123', 'hzdkv@example.com'),
        (2, 'kaizar', 'pass1', 'asd@example.com'),
        (3, 'ammar', 'something', 'aeh@example.com'),
        (4, 'amin', 'random', 'auwhg@example.com')
"""



def user_pos(user):
    res = cur.execute("SELECT username FROM det")
    usertup = res.fetchall()

    for i,use in enumerate(usertup):
        if convertTuple(usertup[i]) == user:
            return i
    return -1
    
def code_gen(user):
    if user_pos(user) == -1:
        print("user not found")
        exit() 
    code = token_urlsafe(32)
    return code
    
def code_checker(user,code,user_inp):#compares the codes to a user inputed code
    if code != user_inp:
        return False
    else:
        return pass_changer(user)
    
def pass_changer(user):
    pos = user_pos(user)
    password = getpass("enter your password")
    while not pass_req(password):
        print("you did not meet req")
        password = getpass("enter your password")
    password = str(hash(password))
    q = "UPDATE det SET password = "+"'"+password+"'"+" WHERE username = "+"'"+user+"'"
    cur.execute(q) 
    con.commit()
    print("password changed")
    

def convertTuple(tup):
        # initialize an empty string
    str = ''
    for item in tup:
        str = str + item
    return str


def hash(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def pass_req(password):# the password requrements(kept it empty for abstraction reasons)
    return True


def get_det():
    cur.execute("SELECT * FROM det")
    return cur.fetchall()

initial = get_det()


us = "amin"
code = code_gen(us) # currently manually inputing the code will do an email thing later

u_i = code # need to inject the parameter here from the online form U_i stands for user input

code_checker(us,code,u_i)





final = get_det()


pprint(initial)
pprint(final)