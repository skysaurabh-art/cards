The following project is about the credit cards used by a user
The project contains 4 python files and 1 database file.
The settings file is used to create the database
The databse file contains two tables, cards_table and the user table
the cgid_tables file contains the creation of cards table and it's columns and various methods we want to perform on the cards table
the users file conatain the users table, which contains the list of authenticated users, using this file, you can add, view the users you want
the app file contains the actual application code.

How to run:
First create database by running settings.py in python 3 or above
check if the database is successfully created of not at the designated loaction
run cgid_tables file
after running the cgid_tables, perform db.create_all() in python, it will create the tables
run users file
after running the users, perform db.create_all() in python, it will create the tables
atlast, run the app.py file, it will start the server 
go to postman, send corresponding requests with reference to the app code, as per your requirements
