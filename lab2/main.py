import getpass
import sys
import os
import json
import hashlib
import uuid


def checkPassFromat(password):
    if (len(password) < 8 or not any(char.isdigit() for char in password) or
            not any(char.isalpha() for char in password) or not any(char.isupper() for char in password) or
            not any(char.islower() for char in password)):
        print("Password must be longer than 8 charactes and must contain small and big letters and numbers")
        return False
    if any(not char.isalnum() for char in password):
        return True

    print("Password must contain special characters")
    return False


def checkSame(user, password):
    if hash(password.encode(), user['salt'].encode()) == user['password']:
        print("New password can not be the same as the current one!")
        return False
    return True


def hash(password, salt):
    return hashlib.sha256(salt + password).hexdigest()


def writeData(new_data, type):
    if type == "add" or type == "passwd":
        pswd = getpass.getpass()
        pswd2 = getpass.getpass("Repeat Password: ")
        if pswd != pswd2:
            print("error! Password missmatch!")
            return
        if not checkPassFromat(pswd):
            return

    with open("logins.json", 'r') as file:
        file_data = json.load(file)

        if type == "add":

            for obj in file_data['users']:
                if obj['username'] == new_data['username']:
                    print("can not have two users with same username")
                    return

            salt = uuid.uuid4().hex.encode()
            new_data['password'] = hash(pswd.encode(), salt)
            new_data['salt'] = salt.decode()

            file_data['users'].append(new_data)

    with open("logins.json", "w") as jsonFile:
        if type == "passwd":
            for obj in file_data['users']:
                if obj['username'] == new_data['username']:
                    obj['password'] = hash(pswd.encode(), obj['salt'].encode())
                    print("Password successfully changed!")

        elif type == "forcepass":
            for obj in file_data['users']:
                if obj['username'] == new_data['username']:
                    obj['flag'] = "1"
                    print("User will be requested to change password on next login.")

        elif type == "del":
            for i in range(len(file_data['users'])):
                if file_data['users'][i]["username"] == new_data['username']:
                    file_data['users'].pop(i)
                    print("User successfuly removed.")
                    break

        json.dump(file_data, jsonFile, indent=4)

        if type == "add":
            print(f"user {new_data['username']} sucsessfully added")


def findRecord(username):
    if not os.path.exists("logins.json"):
        with open("logins.json", "w") as file:
            initial_data = {"users": []}
            json.dump(initial_data, file)
        return {"username": username, "password": "", "salt": "", "flag": "0"}

    with open("logins.json", 'r') as file:
        file_data = json.load(file)

        for obj in file_data['users']:
            if obj['username'] == username:
                return {"username": username, "password": obj['password'], "salt": obj['salt'], "flag": obj['flag']}

        return {"username": username, "password": "", "salt": "", "flag": "0"}


def changeUserPass(user):
    pswd = getpass.getpass("New Password: ")
    pswd2 = getpass.getpass("Repeat New Password: ")

    if pswd != pswd2:
        print("error! Password missmatch!")
        return False

    if not checkPassFromat(pswd):
        return False

    if not checkSame(user, pswd):
        return False

    with open("logins.json", "r") as File:
        file_data = json.load(File)

    with open("logins.json", "w") as jsonFile:
        for obj in file_data['users']:
            if obj['username'] == user['username']:
                salt = uuid.uuid4().hex.encode()
                obj['password'] = hash(pswd.encode(), salt)
                obj['salt'] = salt.decode()
                obj['flag'] = "0"
                json.dump(file_data, jsonFile, indent=4)
                print("Login Successfull!")
                return True
    return False


def login(user):
    while True:
        pswd = getpass.getpass()
        if hash(pswd.encode(), user['salt'].encode()) == user['password']:
            if user['flag'] == "1":
                newpass = changeUserPass(user)
                return newpass
            else:
                print("Login Successfull!")
                return True
        else:
            print("Wrong Username or Password!")


if __name__ == '__main__':
    args = sys.argv[1:]
    if args[0] == "usermgmt":
        user = findRecord(args[2])
        writeData(user, args[1])

    elif args[0] == "login":
        user = findRecord(args[1])
        login(user)





