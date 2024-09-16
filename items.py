import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint

if __name__ == "__main__":
    num = 18
    lists = []
    for page in range(500):
        url = f"https://spa5.scrape.center/api/book/?limit={num}&offset={num*page}"
        r = requests.get(url)
        j = r.json()["results"]
        lists = [*lists , *[item["name"] for item in j]]
        print(f"第{page+1}页完成")
    print(f"一共有 {len(lists)} 关键字")
    with open("items.txt", "w", encoding="utf-8") as f:
        json.dump(lists, f, indent=4, ensure_ascii=False)