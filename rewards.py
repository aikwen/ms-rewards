import json, random, sys
import cookies
from loguru import logger

def random_seconds():
    return random.randint(150, 300)

def get_words():
    with open("items.txt", "r", encoding="utf-8") as f:
        li = json.load(f)
    return li

def search(page, word):
    page.goto("https://cn.bing.com/")
    page.wait_for_load_state("load")
    seconds = random_seconds()
    page.get_by_role("searchbox", name="输入搜索词").click()
    page.get_by_role("searchbox", name="输入搜索词").fill(f"{word}")
    page.get_by_role("searchbox", name="输入搜索词").press("Enter")
    logger.info(f"wait for {seconds} seconds, key: {word}")
    page.wait_for_timeout(seconds * 1000)
    

def main():
     words = get_words()
     with cookies.open_browser(headless=True) as b:
            with b.new_context() as c:
                # 导入 cookies
                if cookies.load_cookies(c) is None:
                    print("cookies.txt not found")
                    sys.exit()
                # 打开页面开始搜索
                with c.new_page() as page:
                    for _ in range(10):
                        word = random.choice(words)
                        search(page, word)

if __name__ == '__main__':
    main()
