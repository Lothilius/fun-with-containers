# Hypothetical Problem Statement
## Given the CSV attached in this email:
- []	Create a new db (SQL RDS e.g. postgresl, sqlite)
- []	Import the "users" CSV file into a new db table called “users”.
- []	Create a new table named "daily_user_counts". The new table should have 5 columns, year, month, day, observed, count). 
- [] Create a Python3 script that:
    - [] Reads "users" table into a pandas dataframe.
    - [] Count the number of users by day.
    - [] Then calculate the number of users expected to signup 1 day into the future. 
    > **Note** a simple mean/average is sufficient for communicating an expected value. 
    - [] Append the new record with the expected count to the dataframe.
    - [] Load/Insert the results of your calculations (the dataframe) into your "daily_user_counts" table.

## Considerations

### Assumptions


## Solution
 
