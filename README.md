# Hypothetical Problem Statement
## Given a specific CSV:
id (string) | first_name (string) | last_name (string) | age (integer) | gender (string) | visit_date (date) 
------------ | ------------ | ------------- | ------------- | ------------ | ------------- 

- [x]	Create a new db (SQL RDS e.g. postgresl, sqlite)
- [x]	Import the "users" CSV file into a new db table called “users”.
- []	Create a new table named "daily_user_counts". 
The new table should have 5 columns, year, month, day, observed, count). 
- [] Create a Python3 script that:
    - [] Reads "users" table into a pandas dataframe.
    - [] Count the number of users by day.
    - [] Then calculate the number of users expected to signup 1 day into the future. 
    **Note** a simple mean/average is sufficient for communicating an expected value. 
    - [] Append the new record with the expected count to the dataframe.
    - [] Load/Insert the results of your calculations (the dataframe) into your "daily_user_counts" table.

## Assumptions
1. The above request is needed to solve a problem and the above outlines the "best" solution considered
1. The solution will be considered a one-off solution used to solve for an edge case
1. In a typical implementation, a docker container would likely not be used for the PostgreSQL db but instead would be 
deployed to RDS
1. The csv file contains sensitive data
1. The id column is made of two ids a user id and possibly last four of a social
1. The analysis of the user data would be needed on a repeated schedule 



## Considerations
1. Security - Are there any guidelines in place to enforce HIPPA compliance and/or other security standards?
1. Speed to deploy vs Repeatability - Because it is being considered as a one-off speed is favored over being able to 
recreate multiple times. 
1. Because of the interesting user id the full id is needed for uniqueness. 
    1. The second section of the id can have a leading zero so it is treated a string
    1. When addressing uniqueness the original id structure is needed.
1. Forecasting the number of users expected to signup the next would likely be a repeated need so it would make sense to 
impliment a class
    

## How to Run 
1. Set environment variables like in the following example. They will be called by the env.list files.  
Example:
    ```bash
    export POSTGRES_USER="some_user_name"
    export POSTGRES_PASSWORD="some_super_secret_pw"
    export CSV_FILE="/full/path/to/file.csv"
    export POSTGRES_HOST
    ```
1. Run the following from the Root directory to build and run the postgres database and load the csv in to the db  
    ```bash
    docker-compose -f docker-compose.yaml up
   ``` 
1. Instructions to create processing container 
