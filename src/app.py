import io
import logging
import pathlib
import re
import time
import urllib.parse
from typing import Optional

import requests

from selenium import webdriver

logger = logging.Logger("app-loger")
url = 'https://www.instagram.com/LimitlessMacey/?hl=en'

# TODO: Parse beacons.ai, parse lnk.bio
# TODO: Parse profiles that have multiple @s on their profile which end up in the funny link
# Todo: Add search mode + append mode


def app():
    # beacons / lik.bio / link.tree / bitly

    username = url.strip().split("/")[3].lower()
    profiles_path = str(pathlib.Path().absolute())

    # make sure it's saved for testing purposes because IG blocks it otherwise
    if profile_available_local(profiles_path, username):
        content = open(profiles_path + f"/data/profiles/{username}.txt", "r").read()
    else:
        content = selenium_get_content(url, as_headless=False)
        saved = save_content(content, profiles_path, username)
        if not saved:
            logger.error("Error saving profile")

    if not content:
        logger.error("Profile not found or not defined")
        return False

    logger.info(f"Profile found: {url}")
    found_links = identify_provider(content)

    # return provider
    if not found_links:
        logger.error("Provider not found or not defined")
        return False

    logger.info(f"Protential provider of funny content found: {found_links}")

    # returns parsed page
    funny_results = investigate_providers(found_links)

    if not funny_results:
        logger.info("Congratulations, you have not been faned, you are safe my brother/sister in Christ.")
        return False
    else:
        logger.info("I am sorry my brother/sister in Christ, you have been faned, he/she is for the streets.")

    return True


def save_content(content: str, base_path: str, username: str) -> bool:
    open(base_path + f"/data/profiles/{username}.txt", "w").write(content)
    return profile_available_local(base_path, username)


def profile_available_local(base_path: str, username: str) -> bool:
    return pathlib.Path(base_path + f"/data/profiles/{username}.txt").exists()


def as_headless(options: webdriver.ChromeOptions) -> webdriver.ChromeOptions:
    options.add_argument("--headless=new")
    return options


def requests_get_content(url: str) -> str:
    r = requests.get(url)
    if r.status_code != 200 or r.content is None or r.content == "":
        return ""

    return r.content.decode("utf-8")


def selenium_get_content(url: str, **kwargs) -> str:
    options = webdriver.ChromeOptions()

    if kwargs.get("as_headless", ""):
        options = as_headless(options)

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(20)
    source = str(driver.page_source)
    driver.quit()

    del driver

    if not source:
        logger.warning("Page empty or does not exist")
        return ""

    return source


def identify_provider(content: str) -> list[Optional[list]]:

    providers = {
        "linktr.ee": r"https%3A%2F%2Flinktr.ee%2F[a-zA-Z_-]+",
    }

    found_providers = []

    for key, value in providers.items():
        link = re.findall(value, content)

        # check when it comes directly from <span>{link}<span>
        if link:
            decoded = urllib.parse.unquote(link[0])
            if decoded:
                found_providers.append([key, decoded])
            else:
                logger.warning(f"Might have a link but failed to decode: {link}")

    return found_providers


def investigate_providers(links: list[list]) -> list[Optional[dict]]:
    has = []
    for link in links:
        content = ""
        if "beacons" in link[0]:
            content = selenium_get_content(link[1], as_headless=False)

        if "linktr" in link[0]:
            content = requests_get_content(link[1])

        of_link = has_onlyfans(content)
        if of_link:
            has.append({"source": "onlyfans", "url": of_link})

    return has


def has_onlyfans(content: str) -> str:
    link = re.findall(r"https://onlyfans.com/[A-Za-z_-]+", content)

    if link:
        link = list(set(link))  # OF requests.get returns 2 links sometimes, deduplicate

        return link[0]

    return ""


def has_fansly(content: str) -> str:
    pass


def has_twitter(url: str) -> str:
    pass
