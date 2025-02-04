import requests
from bs4 import BeautifulSoup
import json

config = json.loads(open("config.json").read())

class DateInformation:
    def __init__(self, day: str, food_items: list[str]) -> None:
        self.date = day
        self.food = food_items
                
    def get_json(self):
        return {
            "date": self.date,
            "food": self.food
        }
        
def fetch_menu_html():
    html = requests.get(config["url"])
    return BeautifulSoup(html.text, 'html.parser')

def scrape_menu_json(soup: BeautifulSoup) -> list[DateInformation]:
    menu_items = []
    
    # Process only the main tag
    main_content = soup.find("main", id="main")
    if not main_content:
        return menu_items
    
    # Find all <p> tags containing <strong> for day names
    for paragraph in main_content.find_all("p"):
        strong_tag = paragraph.find("strong")
        if strong_tag:
            day_name = strong_tag.text.strip()
            
            # Find the next sibling which should be a <ul> containing menu items
            ul = paragraph.find_next_sibling("ul")
            
            if ul:
                food_items = [li.text.strip() for li in ul.find_all("li")]
                menu_items.append(DateInformation(day_name, food_items))
    
    return menu_items
