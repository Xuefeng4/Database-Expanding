# Database-Expanding

## Purpose
This program simulates a scenario for Emlab Solutions which could expand an existing database to store user subscription data for software further development

## Step Explanation
Step 1: Connect the MongoDB server. Please change the connection string to yours while testing <br>
Step 2: Create a new database called emlab <br>
Step 3: Create some sample data for the initial database <br>
Step 4, Create a collection called account to store initial user data and insert the randomly generated sample data into it <br>
Step 5, Expand the database field by adding a new filed for subscription in account collection <br>
Step 6, Create a new collection of subscription, generate sample data and create a reference between the two collections <br>
Step 7, Simulate a scenario when we want to check if a user is just a visitor or prime member<br>

## Design Pattern
The initial database originally stores basic user information in a collection(similar as a table in SQL database).
To add more subscription data, I created a new collection to only store specific data of subscription, e.g., start date and expire date, then I created a reference between the two collections by adding each subscription id as a foreign key into the account collection's relevant field. So the developer could easily check the subscription data of the corresponding user by the reference 

The reason I did not store the subscription data into the account collection directly is that as time goes by, the subscription history could be very large, if we store them together, it could lower the processing speed and handicap the data retrieval of other information.

The two tables could be explained as below in a SQL model

Account

| Attribute | Value |
| --------- | ----- |
| id | primary key |
| user name | unique string |
| email | unique string |
| password | hashed sting | 
| subscription | array of subscription id | 

Subscription

| Attribute | Value |
| --------- | ------ |
| id | primary key |
| start date | python date object |
| end date | python date object |

## Test Instruction
For testing, run MongoDB locally and change the collection string to your own in the program.
The result of each stage would be printed in the terminal

