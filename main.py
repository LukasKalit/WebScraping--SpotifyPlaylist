import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

Client_ID = os.getenv("Client_ID")

# date = input("Chose a day you want to travel YYYY-MM-DD: ")
# print(date)

html_doc = f"https://www.billboard.com/charts/hot-100/2000-08-12/"

response = requests.get(html_doc)
response.status_code

soup = BeautifulSoup(response.text, "html.parser")


links = soup.find_all(class_="o-chart-results-list-row-container")
list_of_titles = [row.find("h3").string.strip() for row in links]

# print(links)
print(list_of_titles)
print(len(list_of_titles))

