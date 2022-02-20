import requests
from bs4 import BeautifulSoup

LIMIT = 50

def get_last_page(url):
  result = requests.get(url+"0")
  soup = BeautifulSoup(result.text, "html.parser")
  pages = soup.find("div", {"class": "pagination"}).find_all('a')
  while pages[-1].string is None:
    result = requests.get(url+f"{50*int(pages[-2].string)}")
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "pagination"}).find_all('a')
  return int(pages[-1].string)
 

def processing_jobs(html):
    info_including_title = html.find("h2",class_="jobTitle")

    title = info_including_title.find("span", title=True).string
    
    if html.find("span", {"class": "companyName"}) is not None:
      company = html.find("span", {"class": "companyName"}).string
    else:
      company = "None"

    location = html.find("div", {"class" : "companyLocation"}).string

    job_id = html["data-jk"]

    return {
      'title': title,
      'company' : company,
      'location' : location,
      'link' : f"https://www.indeed.com/viewjob?jk={job_id}"
    }

def extract_jobs(last_page, url):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping Indeed: page {page + 1}")
    result = requests.get(f"{url}&start={page*LIMIT}")
    soup= BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("a",{"class": "fs-unmask"})

    for result in results:
      job = processing_jobs(result)
      jobs.append(job)
      
  return jobs

def get_jobs(word):
  url = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit={LIMIT}&start="
  last_page = get_last_page(url)
  jobs = extract_jobs(last_page, url)
  return jobs