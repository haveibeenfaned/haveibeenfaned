import os
import re
import time
from typing import List

import requests
from selenium import webdriver

from providers import Provider


def requests_get_content(url: str, headers: dict = {}) -> str:
    r = requests.get(url, headers=headers)
    if r.status_code != 200 or r.content is None or r.content == "":
        return ""

    return r.content.decode("utf-8")


def as_headless(options: webdriver.ChromeOptions) -> webdriver.ChromeOptions:
    options.add_argument("--headless=new")
    return options


def selenium_get_content(url: str, **kwargs) -> str:
    options = webdriver.ChromeOptions()

    if kwargs.get("as_headless", ""):
        options = as_headless(options)

    user_data_dir = os.getenv("USERDATADIR", '"/Users/d37998/Library/Application Support/Google/Chrome/Default"')
    options.add_argument(f'--user-data-dir={user_data_dir}')
    driver = webdriver.Chrome(options=options)
    time.sleep(5)
    driver.get("https://www.instagram.com/")
    time.sleep(3)
    driver.get(url)
    time.sleep(10)
    source = str(driver.page_source).lower()
    time.sleep(2)
    driver.quit()

    return source


def re_get_exceptions(content_providers: List[Provider], content: str) -> str:
    ex = ""
    for provider in content_providers:
        for exception in provider.exceptions:
            ex = re.findall(exception["find"], content)
            if ex: ex = exception["response"]

    return ex


# Nice right?
def re_get_content(content_providers: List[Provider],
                   content: str) -> list:
    found_providers = []

    for provider in content_providers:

        for pattern in provider.link_finders:
            link = re.findall(pattern["find"], content)

            # check for exceptions such as profile non existant (Provider.exceptions)

            if not link:
                continue

            link = link[0]
            if pattern["post"]:
                link = pattern["post"].__call__(link)

            found_providers.append([provider, f"https://{link}"])
            break

    return found_providers


def get_provider_content(url: str) -> str:
    content = ""  # TODO: Adapt to multiple contents
    if "beacons" in url:
        content = selenium_get_content(url, as_headless=False)

    if "linktree" in url:
        content = requests_get_content(url)

    if "lnk" in url:
        content = selenium_get_content(url, as_headless=False)

    if "allmylinks" in url:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        content = requests_get_content(url, headers=headers)

    return content
