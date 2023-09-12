# NCAA Baseball Statistics Scraper

## Overview

This script is designed to scrape NCAA Baseball statistics and save them in a CSV file named `AllSeasons.csv`.

## Prerequisites

- Python 3.x
- Selenium WebDriver
- BeautifulSoup4
- Pandas
- lxml

To install all the required Python packages, run the following command:

```bash
pip install selenium beautifulsoup4 pandas lxml


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import os


# This section of code checks if a CSV file named "AllSeasons.csv" exists.
# If it does, it loads the existing data into a DataFrame. Otherwise, a new DataFrame is created.
if os.path.exists("AllSeasons.csv"):
    all_season_data = pd.read_csv("AllSeasons.csv")
else:
    all_season_data = pd.DataFrame()


# This function sets up the Selenium WebDriver using Chrome and returns the driver object.
# The driver is configured to wait for 20 seconds after each command.
def setup_browser():
    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(20)
    return driver

# This function interacts with the drop-down menus on the webpage to select values for the sport, academic year, and division.
def select_values_from_dropdowns(driver, selected_season):
    Select(driver.find_element(By.NAME, 'sport')).select_by_visible_text('Baseball')
    Select(driver.find_element(By.NAME, 'acadyr')).select_by_visible_text(selected_season)
    Select(driver.find_element(By.NAME, 'u_div')).select_by_visible_text('I')


# This function scrapes the data from the table and returns it as a list of lists.
# Each sublist contains information for a single row of the table.
def extract_data_from_table(soup):
    base_url = "https://stats.ncaa.org"
    table_rows = soup.select('#rankings_table tbody tr')
    all_data = []
    # ... (explanation for the loop and data extraction)
    return all_data

# The main function orchestrates the overall web scraping process.
# It iterates through all seasons, sets up the browser, makes selections, and extracts data.
def main():
    url = 'https://stats.ncaa.org/rankings/change_sport_year_div'
    seasons = [f"{year}-{str(year+1)[-2:]}" for year in range(2010, 2023)]
    # ... (rest of the function)


# This section is the entry point of the script.
# It calls the main function and handles any exceptions that may occur.
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error occurred: {e}")

python ncaa_stats_scraper.py



Feel free to update this README.md as you see fit for your project.
