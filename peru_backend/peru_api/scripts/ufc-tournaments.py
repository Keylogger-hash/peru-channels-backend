import requests
from bs4 import BeautifulSoup
import json 
url = "https://fightingtomatoes.com/API/490a935d7e46847597c1da2cf1f1383d745d01b7/any/any/any"
r = requests.get(url)
soup = BeautifulSoup(r.content,"html.parser")
data = soup.text.replace('\n','').replace('UFC Data API Endpoint','')
json_data = json.loads(data)

events = []
print(json_data)