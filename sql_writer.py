import pymysql
from csv import reader
import os

# Sets up the connection object
connectionObject = pymysql.connect(host="",
                                   user="",
                                   password="",
                                   db="")

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

  sqlQ = "DROP TABLE IF EXISTS Jobs"
  connectionObject.commit()
  cursorObject.execute(sqlQ)

  # SQL query string
  sqlQuery = "Create TABLE Jobs(id INT PRIMARY KEY AUTO_INCREMENT, applied BOOLEAN DEFAULT FALSE, title VARCHAR(255), company VARCHAR(255), summary TEXT(1000), url TEXT(1000))"

  # Execute the sqlQuery
  cursorObject.execute(sqlQuery)

  for job in jobs:
    # checkt to make sure jobs are unique by varifying url
    existsSql = "SELECT COUNT(*) AS count FROM Jobs WHERE url = '%s'" % (
        job[4])
    cursorObject.execute(existsSql)
    dup = cursorObject.fetchone()[0]
    # if the url is unique add it to the database and the company is not revature
    if(dup == 0 and job[2] != "Revature"):
      sql = 'INSERT into Jobs(title, company, summary, url) VALUES("%s", "%s", "%s", "%s");' % (
          job[1], job[2], job[3], job[4])
      cursorObject.execute(sql)
      # connection is not autocommit by default. So you must commit to save
      # your changes.
      connectionObject.commit()


except Exception as e:

  print("Exeception occured:{}".format(e))

finally:

  connectionObject.close()
