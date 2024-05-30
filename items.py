import requests
import json
from bs4 import BeautifulSoup


if __name__ == "__main__":
    r = requests.get("https://www.runoob.com/note/40199")
    soup = BeautifulSoup(r.text, "html.parser")
    li = soup.find("div", class_="cate-items").find_all("a")
    li = [i.text for i in li]
    with open("items.text", "w", encoding="utf-8") as f:
        f.write(json.dumps(li))
