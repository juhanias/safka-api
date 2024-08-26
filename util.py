import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
import json

config = json.loads(open("config.json").read())

class DateInformation:
    def __init__(self, html: Tag) -> None:
        portions: list[Tag] = html.find_all("td")
        self.date = portions[0].text
        food = portions[1].find_all("p")
        self.food = [entry.text.replace(u"\xa0", "").strip() for entry in food]
        self.food = [entry for entry in self.food if entry != ""]
                
    def get_json(self):
        return {
            "date": self.date,
            "food": self.food
        }
        
def fetch_menu_html():
    html = requests.get(config["url"])
    return BeautifulSoup(html.text, 'html.parser')

def scrape_menu_json(soup: BeautifulSoup) -> list[DateInformation]:
    table_bodies = soup.find_all("tbody")[0]
    dates = table_bodies.find_all("tr")
    
    return [DateInformation(date) for date in dates]    
