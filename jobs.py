import requests
import re
from bs4 import BeautifulSoup
from csv import writer

city = input("Enter A City name: ")
state = input("Enter A State Abbreviation: ")

url = "https://www.indeed.com/jobs?q=software+engineer&l={}%2C+{}&explvl=entry_level".format(city, state)
# Set to hold jobs to avoid duplicates
jobSet = set()
# Regex to find special characters
specChars = re.compile(r'[,|\n"\'\"\r]')

# Loops through the first 18 pages of linkedin
for count in range(0, 18):
    results = requests.get(url)
    soup = BeautifulSoup(results.text, "html.parser")
    jobResults = soup.select("#resultsCol .result")
    nextL = soup.select(".pagination a")
    for job in jobResults:
        original = 0
        anchor = job.select("a")
        title = anchor[0]["title"]
        link = "https://www.indeed.com/" + anchor[0]["href"]
        job_page = requests.get(link)
        job_soup = BeautifulSoup(job_page.text, "html.parser")
        postlink = job_soup.select("#originalJobLinkContainer > a")
        if postlink:
            link = postlink[0]["href"]
            original = "1"
        company = job.select(".company")[0].text.strip()
        summary = job.select(".summary")[0].text.strip()
        fullPost = ["0", str(original), title, company, summary, link]
        cleanPost = [re.sub(specChars, '', i.strip()) for i in fullPost]
        joinedPost = ",".join(cleanPost)
        jobSet.add(joinedPost)
    url = "https://www.indeed.com/" + nextL[len(nextL)-1]["href"]

# Creates a new CSV file
out = open("jobs.csv", "w")

# write the headers for the csv
["applied", "original", "title", "company", "summary", "link"]
out.write("applied,original,title,company,summary, link\n")

# adds each Post as a line in the csv file
for job in jobSet:
    out.write(job + "\n")
