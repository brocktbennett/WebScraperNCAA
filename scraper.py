from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import os

# Load existing data if available
if os.path.exists("AllSeasons.csv"):
    all_season_data = pd.read_csv("AllSeasons.csv")
else:
    all_season_data = pd.DataFrame()

def setup_browser():
    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(20)
    return driver

def select_values_from_dropdowns(driver, selected_season):
    Select(driver.find_element(By.NAME, 'sport')).select_by_visible_text('Baseball')
    print("The Sport Baseball Selected")

    Select(driver.find_element(By.NAME, 'acadyr')).select_by_visible_text(selected_season)
    print(f"Date {selected_season} selected")

    Select(driver.find_element(By.NAME, 'u_div')).select_by_visible_text('I')
    print("Division 1 Selected")

def extract_data_from_table(soup):
    base_url = "https://stats.ncaa.org"
    table_rows = soup.select('#rankings_table tbody tr')

    all_data = []
    for row in table_rows:
        columns = row.select('td')
        data = {
            "rank": columns[0].text.strip(),
            "team_name": columns[1].a.text.strip(),
            "team_link": base_url + columns[1].a['href'],
            "wins": columns[2].text.strip(),
            "losses": columns[3].text.strip(),
            "ties": columns[4].text.strip(),
            "pct": columns[5].text.strip()
        }
        all_data.append([data[key] for key in data])

    return all_data

def main():
    url = 'https://stats.ncaa.org/rankings/change_sport_year_div'

    # Generate the list of seasons
    seasons = [f"{year}-{str(year+1)[-2:]}" for year in range(2010, 2023)]

    for selected_season in seasons:
        with setup_browser() as driver:
            driver.get(url)
            select_values_from_dropdowns(driver, selected_season)
            driver.find_element(By.XPATH, "//*[text()='Team']").click()
            print("'Team' column selector clicked")
            Select(driver.find_element(By.NAME, 'Stats')).select_by_visible_text('WL Pct')
            print("'WL Pct' statistics type selected")
            time.sleep(1)
            Select(driver.find_element(By.XPATH, "//select[@name='rankings_table_length']")).select_by_index(3)
            print("'Max entries' column selector clicked")
            soup = BeautifulSoup(driver.page_source, 'lxml')

        all_data = extract_data_from_table(soup)

        for entry in all_data:
            entry.append(selected_season)

        df = pd.DataFrame(all_data, columns=['Ranking', 'Team Name', 'Hyperlink', 'Wins', 'Losses', 'Ties', 'Winning Percentage', 'Season'])

        # Append new data to global DataFrame
        global all_season_data
        all_season_data = pd.concat([all_season_data, df], ignore_index=True)

    # Save all data after finishing all seasons
    save_path = os.path.join(os.getcwd(), "AllSeasons.csv")
    all_season_data.to_csv(save_path, index=False)
    print("All data exported to AllSeasons.csv")

    # Append the timestamp to the end of the CSV file
    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(save_path, 'a') as f:
        f.write(f"\nData extraction completed on: {current_timestamp}\n")

    print(f"Data extraction timestamp added: {current_timestamp}")
    print("Exiting script.")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error occurred: {e}")
