from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
START_URL = 'https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars'
browser = webdriver.Chrome()
browser.get(START_URL)

new_sun_data = []


def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)

        soup = BeautifulSoup(page.content, "html.parser")

        temp_list = []

        for tr_tag in soup.find_all("tr", attrs={'class': 'fact_row'}):
            td_tags = tr_tag.find_all('td')

            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all(
                        'div', attrs={'class': 'value'}
                    )[0].contents[0])
                except:
                    temp_list.append("")
        new_sun_data.append(""
                            )
    except:
        scrape_more_data(hyperlink)


planet_df_1 = pd.read_csv('updated_scraped_data.csv')

for index, row in planet_df_1.iterrows():
    print(row['hyperlink'])
    scrape_more_data(row['hyperlink'])
    print(f"data scraping at hyperlink {index+1} completed")

scrapped_data = []

for row in new_sun_data:
    replaced = []
    for el in row:
        el = el.replace("\n", "")
        replaced.append(el)
    scrapped_data.append(replaced)

print(scrapped_data)

headers = ['star_name', 'radius', 'mass', 'distance']
new_planet_df_1 = pd.DataFrame(scrapped_data, columns=headers)
new_planet_df_1.to_csv('new_scraped_data.csv', index=True, index_label='id')
