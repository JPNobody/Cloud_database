# Overview

The software that I wrote is used to access a cloud database that has accounts and recipes for each account. 
 This software uses a private key to be able to access the database. My program uses a commandline interface to create accounts, sign into the accounts, add recipes, update recipes, delete recipes, edit the account, and delete the account. This program stores the passwords for each account using a hashing library in order to be more secure. 

The purpose of this project is to help me, learn and understand more about cloud databases, specifically with the firestore database type. I also want to learn more about security of cloud databases and password storage. 

{Provide a link to your YouTube demonstration.  It should be a 4-5 minute demo of the software running, a walkthrough of the code, and a view of the cloud database.}

[Software Demo Video](https://youtu.be/wc34Fcz4hbc)

# Cloud Database

I am using the firestore database.

The structure of the database is that there is a collection of accounts. Each account has a name and two subcollections. A recipes subcollection, for storing the recipes that a user inputs, and a password subcollection to keep the password more secure. Each recipe has three parts, the title, the ingrediants, and the directions. Each of these are stored in the document. The title is a string. The ingrediants is a dictionary, and the directions are a string with endlines for formatting. 

# Development Environment

For this project I used Visual Studio Code.

I used the Python programming language with the obvious firestore-admin libraries, 
along with the getpass and hashlib libraries for password security. 

# Useful Websites

* [Official Fire-base website](https://firebase.google.com/docs/firestore/quickstart)
* [Stack Overflow on Creating subcollections](https://stackoverflow.com/questions/47514419/how-to-add-subcollection-to-a-document-in-firebase-cloud-firestore)
* [Python Explaination of Hashing](https://docs.python.org/3/library/hashlib.html)

# Future Work

* The biggest thing that I need to fix in the future is with the account names. Each account id is the account name, and this is true for all the documents in the database. This makes it more complicated to update or change the names for the accounts. I could fix this by changing the ids to be randomly generated, but I would also need to rewrite a bunch of code to make it so the program works with those ids.
* In the future I would like to set up security rules with firebase to make the database more secure. I would also like to look more into hashing to make sure that I am using the right type of hash. Along these lines, I would need to implement a better password recovery system then the one I currently have in place. 
* I would also like to hook this database up to a webpage in the future so that I could be something that people actually use to store recipes across large distances. 