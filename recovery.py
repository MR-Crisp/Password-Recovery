from getpass import getpass
import bcrypt
from secrets import *
import sqlite3


def conect():
    con = sqlite3.connect("userdetails.db", check_same_thread=False)
    cur = con.cursor()
    return cur


"""INSERT INTO TBL_users VALUES(1, 'aamir', 'qwerty123', 'aka.amin2005@gmail.com','auwgiuawgiuw'),
        (2, 'kaizar', 'pass1', 'asd@example.com','aywgauwguga'),
        (3, 'ammar', 'something', 'aeh@example.com','awufgaiugflauwgfla'),
        (4, 'amin', 'random', 'auwhg@example.com','awiufgaiufgaiugwf;uaf')"""


def user_exist(email):
    """
    Checks if a user with the given email address exists in the database.

    Args:
        email (str): Email address of the user.

    Returns:
        bool: True if a user with the given email address exists in the database, False otherwise.
    """
    cur = conect()
    cur.execute("SELECT * FROM TBL_users WHERE email =?", (email,))
    user = cur.fetchone()
    if user is not None:
        return True
    else:
        return False


def code_gen(email):
    cur = conect()

    if not user_exist(email):
        return False
    code = token_urlsafe(32)
    cur.execute("UPDATE TBL_users SET code =? WHERE email =?", (code, email))
    return True


def code_checker(email, user_input):  # compares the codes to a user inputed code
    cur = conect()

    if not user_exist(email):
        return False
    cur.execute("SELECT code FROM TBL_users WHERE email =?", (email,))
    code = cur.fetchone()
    code = code[0]
    if code == user_input:
        return True
    else:
        return False


def pass_changer(email):
    """
    Prompts the user to input a new password and if it meets the password requirements,
    hashes and updates the user's password in the database.

    Args:
        email (str): Email address of the user.

    Returns:
        None
    """
    cur = conect()

    password = getpass("enter your password")
    while not pass_req(password):
        print("you did not meet req")
        password = getpass("enter your password")
    password = str(hash(password))
    cur.execute("UPDATE TBL_users SET password =? WHERE email =?", (password, email))
    con = sqlite3.connect("userdetails.db", check_same_thread=False)

    con.commit()
    print("password changed")


def hash(password):
    """
    Generates a salted hash of the given password using the `bcrypt` library.

    Args:
        password (str): A plain-text password.

    Returns:
        str: A salted hash of the given password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def pass_req(
    password,
):  # the password requrements(kept it empty for abstraction reasons)
    return True


def get_det():
    """
    Returns all rows in the "TBL_users" table.

    Args:
        None

    Returns:
        list: A list of tuples, where each tuple represents a row in the "TBL_users" table.
    """
    cur = conect()

    cur.execute("SELECT * FROM TBL_users")
    return cur.fetchall()


val = code_gen("aka.amin2005@gmail.com", "auwgiuawgiuw")
