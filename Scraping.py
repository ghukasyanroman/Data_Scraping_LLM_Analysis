from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import pandas as pd

# Initialize the data dictionary
data = {
    "url": [],
    "job_title": [],
    "job_type": [],
    "work_mode": [],
    "shift": [],
    "salary": [],
    "company_name": [],
    "company_rating": [],
    "location": [],
    "benefits": [],
    "description": []
}

# Initialize global counter
global_scraped_jobs_count = 0

def scrape_job_details(driver, job_url):
    global global_scraped_jobs_count
    time.sleep(random.uniform(1,5))
    driver.get(job_url)
    
    try:
        job_title = driver.find_element(By.XPATH, '//h1[contains(@class, "jobsearch-JobInfoHeader-title")]').text
    except:
        job_title = None
    
    # Company name extraction
    try:
        company_name = driver.find_element(By.XPATH, '//div[@data-company-name="true" or contains(@class, "css-hon9z8")]').text
    except:
        company_name = None

    # Location extraction
    try:
        location = driver.find_element(By.XPATH, '//div[@data-testid="inlineHeader-companyLocation"]//div').text
    except:
        location = None

    # Company rating extraction
    try:
        company_rating = driver.find_element(By.XPATH, '//div[contains(@class, "css-1unnuiz e37uo190")]').text
    except:
        company_rating = None

    # Salary extraction
    try:
        salary = driver.find_element(By.XPATH, '//span[contains(@class, "css-19j1a75") or contains(@class, "js-match-insights-provider-tvvxwd")]').text
    except:
        salary = None

    # Job type extraction
    try:
        job_type_element = driver.find_element(By.XPATH, '//div[@aria-label="Job type" and contains(@class, "js-match-insights-provider-16m282m e37uo190")]')
        if job_type_element:
            job_type = ' '.join(job_type_element.text.split('\n')[1:])  # Skip the first line if necessary
        else:
            job_type = None
    except Exception:
        job_type = None

    # Shift and schedule extraction
    try:
        shift_element = driver.find_element(By.XPATH, '//div[@aria-label="Shift and schedule" and contains(@class, "js-match-insights-provider-16m282m e37uo190")]')
        if shift_element:
            shift = ' '.join(shift_element.text.split('\n')[1:])  # Skip the first line
        else:
            shift = None
    except Exception:
        shift = None

    # Work mode extraction
    try:
        work_mode_element = driver.find_element(By.XPATH, '//div[contains(@class, "css-17cdm7w eu4oa1w0")]')
        if work_mode_element:
            work_mode = work_mode_element.text
        else:
            work_mode = None
    except Exception:
        work_mode = None

    # Benefits extraction
    try:
        benefits = driver.find_element(By.XPATH, '//div[@id="benefits"]').text
    except:
        benefits = None

    # Description extraction
    # Description extraction
    try:
        description_element = driver.find_element(By.XPATH, '//div[@id="jobDescriptionText" and contains(@class, "jobsearch-JobComponent-description")]')
        description = description_element.text if description_element else None
    except:
        description = None

    # Increment global counter
    global_scraped_jobs_count += 1

    # Append scraped data to the data dictionary
    data["url"].append(job_url)
    data["job_title"].append(job_title)
    data["job_type"].append(job_type)
    data["work_mode"].append(work_mode)
    data["shift"].append(shift)
    data["salary"].append(salary)
    data["company_name"].append(company_name)
    data["company_rating"].append(company_rating)
    data["location"].append(location)
    data["benefits"].append(benefits)
    data["description"].append(description)

    # Print how many jobs have been scraped globally
    print(f"Total jobs scraped: {global_scraped_jobs_count}\n")

driver = webdriver.Chrome()
base_urls = [
    "https://www.indeed.com/jobs?q=Accountant&start=",
    "https://www.indeed.com/jobs?q=Business+Analyst&start=",
    "https://www.indeed.com/jobs?q=Cyber+Security+Specialist&start=",
    "https://www.indeed.com/jobs?q=data+analyst&start=",
    "https://www.indeed.com/jobs?q=data+scientist&start=",
    "https://www.indeed.com/jobs?q=devops+engineer&start=",
    "https://www.indeed.com/jobs?q=financial+analyst&start=",
    "https://www.indeed.com/jobs?q=hr+assistant&start=",
    "https://www.indeed.com/jobs?q=IT+Project+Managment&start=",
    "https://www.indeed.com/jobs?q=machine+learning+engineer&start=",
    "https://www.indeed.com/jobs?q=qa+engineer&start=",
    "https://www.indeed.com/jobs?q=software+engineer&start=",
    "https://www.indeed.com/jobs?q=System+Administrator&start="
]

total_pages =  50
all_job_urls = []
for base_url in base_urls:
    for page in range(total_pages):
        print(f"Start Scraping for {base_url[30:-7]}")
        start_value = page * 10
        url = f"{base_url}{start_value}"
    
        driver.get(url)
        
        time.sleep(3)  # Consider using WebDriverWait for a more robust approach
        job_cards = driver.find_elements(By.CSS_SELECTOR, 'a[data-jk]')
    
        for card in job_cards:
            job_id = card.get_attribute('data-jk')
            job_url = f"https://www.indeed.com/viewjob?jk={job_id}"
            all_job_urls.append(job_url)
    
        print(f"Collected URLs from page {page + 1}")
    print(f"Stoped Scraping for {base_url[30:-7]}\n\n")


seen = set()
result = []
for item in all_job_urls:
    if item not in seen:
        seen.add(item)
        result.append(item)

# Iterate over each job URL and scrape details
for job_url in result:
    scrape_job_details(driver, job_url)
driver.quit()
print('The End')
df = pd.DataFrame(data=data)
df.to_csv("Non_Cleaned_Indeed_Jobs.csv", index = False)