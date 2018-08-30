import pymysql
from csv import reader
import os

# Sets up the connection object
connectionObject = pymysql.connect(host="your info here",
                                   user="your info here",
                                   password="your info here",
                                   db="your info here")

# Sets up the jobs array as an empty array
jobs = []

# opens jobs.csv and adds each job row to the list
with open("jobs.csv") as csv_file:
  csv_reader = reader(csv_file)
  # MOves ahead one step to skip headings
  next(csv_reader)
  for row in csv_reader:
    jobs.append(row)

try:

  # Create a cursor object

  cursorObject = connectionObject.cursor()

  # SQL query string
  # sqlQuery = "Create TABLE Jobs(id INT PRIMARY KEY AUTO_INCREMENT, applied BOOLEAN, title VARCHAR(255), company VARCHAR(255), url VARCHAR(255))"

  # Execute the sqlQuery
  # cursorObject.execute(sqlQuery)
  for job in jobs:
    sql = 'INSERT into Jobs(title, company, url) VALUES("%s", "%s", "%s");' % (
        job[1], job[2], job[3])
    cursorObject.execute(sql)
    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connectionObject.commit()


except Exception as e:

  print("Exeception occured:{}".format(e))

finally:

  connectionObject.close()
