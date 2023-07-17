from selenium.webdriver.chrome.webdriver import WebDriver
from bs4 import BeautifulSoup
from typing import Dict, List
import math
from scraper.fetch import fetch_indeed
from handlers.exceptions_handlers import exceptions_handler, timeout_exceptions_handler, timeout_exceptions_screenshot_handler, no_results_exceptions_handler
from handlers.logs_handlers import logs_scraper_handler
from scraper.construct_url import construct_indeed_url
from scraper.extract_indeed import extract_indeed_pages


# Scrapes indeed with the specified job search query terms nad options
@logs_scraper_handler(log_message = f"Scraping Indeed for", log_error_message = "Scraping failed for")
@exceptions_handler
@timeout_exceptions_screenshot_handler
@timeout_exceptions_handler
@no_results_exceptions_handler(job_board = "Indeed")
def scrape_indeed(driver: WebDriver, search_position: str, search_location: str, search_options: Dict[str, str] = None) -> List[Dict[str, str]]:
    # Construct initial indeed url
    initial_url = construct_indeed_url(
        search_position, search_location, search_options)
    
    # Fetch intial indeed url
    fetch_indeed(driver = driver, url = initial_url, initial_fetch = True)

    # Fetch initial HTML and parsed soup
    extracted_html = driver.page_source
    parsed_html = BeautifulSoup(extracted_html, 'html.parser')

    # Extract number of listed jobs, and calculate number of pages
    job_count = parsed_html.find(
        'div', class_='jobsearch-JobCountAndSortPane-jobCount').get_text().split(' ')[0]
    total_page_num = math.ceil(int(job_count) / 15)

    # Extracts job listings data on each page, and then writes/appends them to output json file
    return extract_indeed_pages(driver=driver, search_position=search_position,
                         search_location=search_location, search_options=search_options, total_page_num=total_page_num)