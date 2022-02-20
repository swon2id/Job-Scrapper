import requests
from bs4 import BeautifulSoup

def get_last_page(url):
  result = requests.get(url)
  soup= BeautifulSoup(result.text, "html.parser")
  pages = soup.find("div", {"class": "s-pagination"}).find_all('a')
  last_page = pages[-2].get_text(strip=True)

  return int(last_page)

def processing_jobs(html):
  title = html.find("div", {"class":"fl1"}).find("a").get_text(strip=True)

  company = html.find("div", {"class":"fl1"}).find("h3").find("span").get_text(strip=True)

  location = html.find("div", {"class":"fl1"}).find("h3").find("span", {"class":"fc-black-500"}).get_text(strip=True)

  job_id = html['data-jobid']

  return {
    'title' : title,
    'company' : company,
    'location' : location,
    'link' : f"https://stackoverflow.com/jobs/{job_id}"
  }

def extract_jobs(last_page, url):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping SO: Page {page + 1}")
    result = requests.get(f"{url}&pg={page+1}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class":"-job"})
    for result in results:
      job = processing_jobs(result)
      jobs.append(job)
  return jobs


def get_jobs(word):
  url = f"https://stackoverflow.com/jobs?q={word}"
  last_page = get_last_page(url)
  jobs = extract_jobs(last_page, url)
  return jobs