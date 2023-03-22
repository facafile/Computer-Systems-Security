#!/bin/bash

echo "First we initialise the database by puting a new pair and a chosen masterPass"
python3 lab1.py put MasterPass www.fer.hr 12345678

echo -e "\nWe add 1 more input for good measure"
python3 lab1.py put MasterPass www.google.com testing

echo -e "\nNow we try to input another pair but with a wrong masterPass"
python3 lab1.py put WrongMasterPass www.netflix.com password

echo -e "\nWe will retrive the password for an input in the database"
python3 lab1.py get MasterPass www.fer.hr

echo -e "\nWe will try to retrive a nonexisting input"
python3 lab1.py get MasterPass www.youtube.com

echo -e "\nWe will try to get a existing input using wrong MasterPass"
python3 lab1.py get WrongMasterPass www.google.com

echo -e "\nWe will change an existing input to have a different password and will get it from the database"
python3 lab1.py put MasterPass www.fer.hr newFerPass
python3 lab1.py get MasterPass www.fer.hr

echo -e "\nIf you manualy change any of the required fields in the json file containing the passwords the file will be considered corrupted and will not let you decode it"

