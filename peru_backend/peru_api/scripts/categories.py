import requests
import json

r = requests.get("https://iptv-org.github.io/api/categories.json")

with open("categories.json", "w+") as f:
    data = json.dumps(r.json())
    f.write(data)
