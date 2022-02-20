from scrap_indeed import get_jobs as get_indeed_jobs
from scrap_so import get_jobs as get_so_jobs

def scraping_jobs(word):
  indeed_jobs = get_indeed_jobs(word)
  so_jobs = get_so_jobs(word)
  jobs = indeed_jobs + so_jobs
  return jobs



