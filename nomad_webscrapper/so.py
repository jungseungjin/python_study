import requests
from bs4 import BeautifulSoup

LIMIT = 50
page = 1
URL = f"https://stackoverflow.com/jobs?q=python"

def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text,"html.parser")
    pages = soup.find("div",{"class":"s-pagination"}).find_all("a")
    last_pages = pages[-2].get_text(strip=True)
    return int(last_pages)

def extract_job(html):
    title = html.find("a",{"class":"stretched-link"})["title"]

    #recursive=False 로 첫번째 단계의 span만 가져올 수 있다.
    company, location = html.find("h3",{"class":"fc-black-700"}).find_all("span",recursive=False)

    #아래를 위처럼 써줄 수 있다. 요소가 두개인걸 이미 알 고 있을 때 변수 두개를 잡아넣기
    #company_row = html.find("h3",{"class":"fc-black-700"}).find_all("span",recursive=False)
    #company = company_row[0]
    #location = company_row[1]
    company = company.get_text(strip=True).strip("\n")#안되면 \r 로 해보소
    location = location.get_text(strip=True).strip("-").strip("\n")
    job_id = html["data-jobid"]

    return {"title" : title, "company": company, "location":location, "apply_link":f"https://stackoverflow.com/jobs/{job_id}"}

def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping SO: Page : {page}")
        result = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text,"html.parser")
        results = soup.find_all("div",{"class":"-job"})
        for result in results:
            #result["data-jobid"] -> result의 data-jobid attribute값을 가져올 수 있다.
            job = extract_job(result)
            jobs.append(job)
    return jobs;

def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs