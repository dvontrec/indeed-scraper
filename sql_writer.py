import pymysql
from csv import reader
import os

# Sets up the connection object
connectionObject = pymysql.connect(host=os.environ["HOST"],
                                   user=os.environ["USER"],
                                   password=os.environ["PASSWORD"],
                                   db=os.environ["DATABASE"])
# Sets up the jobs array as an empty array
jobs = []
# opens jobs.csv and adds each job row to the list
with open("jobs.csv") as csv_file:
    csv_reader = reader(csv_file)
    # MOves ahead one step to skip headings
    next(csv_reader)
    for row in csv_reader:
        jobs.append(row)
# Try stuff
try:
    # Create a cursor object
    cursorObject = connectionObject.cursor()
    # If the jobs table exists drop it
    sqlQ = "DROP TABLE IF EXISTS Jobs"
    connectionObject.commit()
    cursorObject.execute(sqlQ)

    # SQL query string
    sqlQuery = "Create TABLE Jobs(id INT PRIMARY KEY AUTO_INCREMENT, applied BOOLEAN DEFAULT FALSE, direct BOOLEAN,  title VARCHAR(255), company VARCHAR(255), summary TEXT(1000), url TEXT(1000))"

    # Execute the sqlQuery
    cursorObject.execute(sqlQuery)
    # Uses list comprehension to filter out revature jobs because they are training courses that require a degree
    jobs = [job for job in jobs if job[3] != "Revature"]
    # loops through all jobs in the jobs array
    for job in jobs:
        sql = 'INSERT into Jobs(direct, title, company, summary, url) VALUES(%s, "%s", "%s", "%s", "%s");' % (job[1], job[2], job[3], job[4], job[5])
        cursorObject.execute(sql)
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connectionObject.commit()

# catch exceptions
except Exception as e:
    # If there is an error print it to the console
    print("Exeception occured:{}".format(e))

# When all is done, close the sql connection
finally:
    connectionObject.close()
