from fastapi import FastAPI
import util
import time

soup = util.fetch_menu_html()
data = util.scrape_menu_json(soup)

cached_response = {
    "last_fetched": int(time.time()),
    "data": data
}

app = FastAPI()

@app.get("/api/v1")
async def root():
    global cached_response
    
    if int(time.time()) - cached_response["last_fetched"] > 60 * 60:
        cached_response = {
            "last_fetched": int(time.time()),
            "data": util.scrape_menu_json(util.fetch_menu_html())
        }
        
    return cached_response
