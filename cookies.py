from playwright.sync_api import sync_playwright
import json
from pathlib import Path

def open_browser(headless=False, milliseconds=1500):
    pw = sync_playwright().start()
    browser = pw.chromium.launch(channel="msedge", headless=headless, slow_mo=milliseconds)
    return browser


def dump_cookies():
    with open_browser() as browser:
        with browser.new_context() as context:
            context.clear_cookies()
            with context.new_page() as page:
                page.on('dialog', lambda dialog: None)
                page.goto("https://cn.bing.com/")
                # wait for bing page load
                page.wait_for_load_state("load")
                print("page loaded")
                # wait for profile image visible
                page.wait_for_selector("id=id_n", state='visible', timeout=1000 * 180)
                cookies = context.cookies("https://cn.bing.com/")
                with open("cookies.txt", "w") as f:
                    json.dump(cookies, f, indent=4)
                    print("cookies saved in cookies.txt")
    return


def load_cookies(context):
    cookie_path = Path(__file__).parent.joinpath("cookies.txt")
    if not cookie_path.exists():
        return None

    with open(f"{cookie_path}", "r") as f:
        cookies_list = json.load(f)
        for cookie in cookies_list:
            if isinstance(cookie["expires"], float):
                cookie["expires"] = int(cookie["expires"])
        context.add_cookies(cookies_list)
    return context

if __name__ == '__main__':
   dump_cookies()
   # print(load_cookies())