import re
import time
from typing import Callable, Union

import requests
from selenium import webdriver


def requests_get_content(url: str, headers: dict = {}) -> str:
    r = requests.get(url, headers=headers)
    if r.status_code != 200 or r.content is None or r.content == "":
        return ""

    return r.content.decode("utf-8")


def selenium_get_content(url: str, **kwargs) -> str:
    options = webdriver.ChromeOptions()

    if kwargs.get("as_headless", ""):
        options = as_headless(options)

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(10)
    source = str(driver.page_source)
    driver.quit()
    time.sleep(10)

    del driver

    if not source or "sorry" in source.lower() or "wrong" in source.lower():
        return ""

    return source


def as_headless(options: webdriver.ChromeOptions) -> webdriver.ChromeOptions:
    options.add_argument("--headless=new")
    return options


# Nice right?
def re_get_content(content_providers: dict[str, list[dict[str, Union[str, Callable[[str], str]]]]],
                   content: str) -> list:
    found_providers = []

    for provider, patterns in content_providers.items():

        for pattern in patterns:
            link = re.findall(pattern["find"], content)

            if not link:
                continue

            link = link[0]
            if pattern["post"]:
                link = pattern["post"].__call__(link)

            found_providers.append([provider, f"https://{link}"])
            break

    return found_providers


def get_provider_content(links: list[list]) -> str:
    content = ""  # TODO: Adapt to multiple contents
    for link in links:
        if "beacons" in link[0]:
            content = selenium_get_content(link[1], as_headless=False)

        if "linktr" in link[0]:
            content = requests_get_content(link[1])

        if "lnk" in link[0]:
            content = selenium_get_content(link[1], as_headless=False)

        if "allmylinks" in link[0]:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            content = requests_get_content(link[1], headers=headers)

    return content
