import requests
from bs4 import BeautifulSoup
from csv import writer

url = "https://www.indeed.com/jobs?q=software+engineer&l=Louisville%2C+KY&explvl=entry_level"

with open("jobs.csv", "w") as file:
  csv_writer = writer(file)
  csv_writer.writerow(["title", "summary", "link"])

  for count in range(0, 5):
    results = requests.get(url)
    soup = BeautifulSoup(results.text, "html.parser")
    jobResults = soup.select("#resultsCol .result")
    nextL = soup.select(".pagination a")
    for job in jobResults:
      anchor = job.select("a")
      title = anchor[0]["title"]
      link = anchor[0]["href"]
      summary = job.select(".summary")[0].text.strip()
      csv_writer.writerow([title, summary, link])

    url = "https://www.indeed.com/jobs?q=software+engineer&l=Louisville%2C+KY&explvl=entry_level" + \
        nextL[len(nextL)-1]["href"]
    print(url)
