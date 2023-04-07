#!/bin/bash

echo "first we are admin and will add a user"
python3 lab2.py usermgmt add testing1

echo -e "\nfirst we are admin and will add another user"
python3 lab2.py usermgmt add testing2

echo -e "\nwe will change the password of testing2 account using admin"
python3 lab2.py usermgmt passwd testing2

echo -e "\nwe will try to log in using new password for testing2 account"
python3 lab2.py login testing2

echo -e "\nwe will delete user testing2 with admin"
python3 lab2.py usermgmt del testing2

echo -e "\nwe will force the user to change his password using admin"
python3 lab2.py usermgmt forcepass testing1

echo -e "\nwe will try to login to account testing1 using wrong password and then the correct one"
python3 lab2.py login testing1

echo -e "\nwe will login to account testing1 using our new password"
python3 lab2.py login testing1

