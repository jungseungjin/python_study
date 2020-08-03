import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&l=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C&radius=50&limit={LIMIT}"

def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all("a")
    pages = []

    for link in links[:-1]:
        pages.append(int(link.find("span").string))

    max_page = pages[-1]
    return max_page;

def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"indeed Scrapping page {page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("div",{"class":"jobsearch-SerpJobCard"})

        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"].strip()
    company = html.find("div", {"class": "sjcl"}).find("span", {"class": "company"}).string
    if company is None:
        company = html.find("div", {"class": "sjcl"}).find("span", {"class": "company"}).find("a").string.strip()
    else:
        company = company.strip()
    # attribute 값을 가져올때 find 뒤에 []를 사용
    location = html.find("div", {"class": "sjcl"}).find("div", {"class": "recJobLoc"})["data-rc-loc"].strip()
    job_id = html["data-jk"]

    return {"title":title , "company" : company , "location" : location,"link":f"https://kr.indeed.com/viewjob?jk={job_id}"}

def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs