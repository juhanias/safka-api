from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import util
import time

soup = util.fetch_menu_html()
data = util.scrape_menu_json(soup)

cached_response = {
    "last_fetched": int(time.time()),
    "data": data
}

app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/api/v1")
async def root():
    global cached_response
    
    if int(time.time()) - cached_response["last_fetched"] > 60 * 60:
        cached_response = {
            "last_fetched": int(time.time()),
            "data": util.scrape_menu_json(util.fetch_menu_html())
        }
        
    return cached_response
