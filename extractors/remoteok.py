from bs4 import BeautifulSoup
from requests import get


def extract_remoteok_jobs(term):
    url = f"https://remoteok.com/remote-{term}-jobs"
    request = get(url, headers={"User-Agent": "Kimchi"})
    if request.status_code == 200:
        results = []
        soup = BeautifulSoup(request.text, "html.parser")
        # write your ✨magical✨ code here
        jobs = soup.find_all("tr", class_="job")
        for job in jobs:
            anchors = job.find_all("a", class_="preventLink")
            anchor = anchors[1]
            link = anchor["href"]
            position = anchor.find("h2")
            company_data = job.find("span", class_="companyLink")
            company = company_data.find("h3")
            regions = job.find_all("div", class_="location")
            if len(regions) == 2:
                region = regions[0].string
            else:
                region = "No Information"
            job_data = {
                "link": f"https://remoteok.com{link}",
                "company": company.string.strip().replace(",", " "),
                "position": position.string.strip().replace(",", " "),
                "region": region.replace(",", " ")
            }
            results.append(job_data)
        return results
    else:
        print("Can't get jobs.")
