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

## Assumptions
1. The above request is needed to solve a problem and the above outlines the "best" solution considered
1. The solution will be considered a one-off solution used to solve for an edge case
1. In a typical implementation, a docker container would likely not be used for the PostgreSQL db but instead would be deployed to RDS
1. The csv file contains sensitive data
1. The id column is made of two ids a user id and possibly last four of a social


## Considerations
1. Security - Are there any guidelines in place to enforce HIPPA compliance and/or other security standards?
1. Speed to deploy vs Repeatability - Because it is being considered as a one-off speed is favored over being able to recreate multiple times. 


## How to Run 
--TODO
 1. Instructions to create postgres db
 docker network create csv_network
 docker build -t load_csv:latest .
docker run -P -h load-csv01 --name load-csv01 -d --env-file env.list --network csv_network load_csv:latest 
1. Instructions to create load container
 1. Instructions to create processing container 
