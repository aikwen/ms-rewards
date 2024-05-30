from playwright.sync_api import sync_playwright
import json, os, random, re, sys, datetime, argparse


def open_browser(milliseconds=1500):
    pw = sync_playwright().start()
    browser = pw.chromium.launch(channel="msedge", headless=False, slow_mo=milliseconds)
    return browser


def get_cookies():
    with open_browser() as browser:
        with browser.new_context() as context:
            context.clear_cookies()
            with context.new_page() as page:
                page.on('dialog', lambda dialog: None)
                page.goto("https://cn.bing.com/")
                # wait for load
                page.wait_for_load_state("load")
                print("页面加载完毕")
                # wait for login
                page.wait_for_selector("id=id_n", state='visible')
                cookies = context.cookies("https://cn.bing.com/")
                with open("cookies.txt", "w") as f:
                    f.write(json.dumps(cookies))
                    print("cookies已保存")
    return


def load_cookies(context):
    if not os.path.exists("cookies.txt"):
        return None

    with open("cookies.txt", "r") as f:
        cookies_list = json.load(f)
        for cookie in cookies_list:
            if isinstance(cookie["expires"], float):
                cookie["expires"] = int(cookie["expires"])
        context.add_cookies(cookies_list)
    return context


def random_seconds():
    return random.randint(180, 300)


def get_current_coin(page):
    page.get_by_label("Microsoft Rewards").click()
    page.wait_for_selector("#rewardsPanelContainer", state="visible")
    text = page.frame_locator("iframe[title=\"Microsoft Rewards\"]").get_by_text("你已获得").first.text_content()
    mat = re.search(r"[0-9]+", text)
    if mat is None:
        return 0
    return mat.group(0)


def search(page, words):
    page.get_by_role("searchbox", name="输入搜索词").click()
    page.get_by_role("searchbox", name="输入搜索词").fill(f"{words}")
    page.get_by_role("searchbox", name="输入搜索词").press("Enter")


def get_words():
    with open("items.text", "r", encoding="utf-8") as f:
        li = json.load(f)
    return li


def main(context):
    li = get_words()
    # print(li)
    coin = 0
    with context.new_page() as page:
        while int(coin) < 90:
            page.goto("https://cn.bing.com/")
            page.wait_for_load_state("load")
            coin = get_current_coin(page)
            seconds = random_seconds()
            words = random.choice(li)
            print(f"{datetime.datetime.now().strftime('[%m-%d %H:%M:%S]')} 当前获得积分:[{coin:>3}/90], ", end=" ")
            if int(coin) >= 90:
                break
            else:
                print(f"下一次搜索在{seconds}秒后, 搜索内容:{words};")
            search(page, words)
            page.wait_for_timeout(seconds * 1000)

        print("结束")


def args_parser():
    parser = argparse.ArgumentParser(description='bing rewards')
    parser.add_argument("-init", '--init_cookies', action="store_true", help='init cookies')
    return parser.parse_args()


if __name__ == '__main__':
    args = args_parser()
    if args.init_cookies:
        get_cookies()
    else:
        with open_browser() as b:
            with b.new_context() as c:
                if load_cookies(c) is None:
                    print("cookies 不存在")
                    sys.exit()
                main(c)
