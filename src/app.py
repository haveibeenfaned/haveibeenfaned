import logging
import pathlib
import re
import sys
import time
import urllib.parse
from typing import Optional

import requests
from selenium import webdriver

logger = logging.getLogger("app-loger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
url = 'https://www.instagram.com/msjennafischer'
logger.addHandler(handler)


# TODO: Parse beacons.ai, parse lnk.bio
# TODO: If no provider found -> return @s linked so you can input those instead
# Todo: Add search mode + append mode


def app():
    # beacons / lik.bio / link.tree / bitly

    username = url.strip().split("/")[3].lower()
    profiles_path = str(pathlib.Path().absolute()) + "/data/profiles/"
    profile_file_path = profiles_path + f"{username}.txt"

    # make sure it's saved for testing purposes because IG blocks it otherwise
    if file_is_local(profile_file_path):
        content = open(profile_file_path, "r").read()
    else:
        content = selenium_get_content(url, as_headless=False)
        saved = save_content(content, profile_file_path)
        if not saved:
            logger.error("Error saving profile")

    if not content:
        logger.error("Profile not found or not defined")
        return False

    logger.info(f"Profile found: {url}")
    found_links = identify_provider(content)

    # return provider
    if not found_links:
        logger.error("Provider not found or profile is not using providers")
        return False

    logger.info(f"Protential provider of funny content found: {found_links}")

    for link in found_links:
        # returns parsed page
        profile_funny_page_file_path = profiles_path + f"{username}_{link[0]}.txt"

        if not file_is_local(profile_funny_page_file_path):
            funny_page = get_provider_content(found_links)

            if not funny_page:
                logger.error("No content found in funny provider link, strange")
                return False

            c = save_content(funny_page, profile_funny_page_file_path)

            if not c:
                logger.error("Could not save funny provider page")
                return False
        else:
            funny_page = open(profile_funny_page_file_path, "r").read()

        of = has_onlyfans(funny_page)
        fansly = has_fansly(funny_page)

        if of or fansly:
            twitter = has_twitter(funny_page)
            logger.info(f"You have been faned: {of}, {fansly}, {twitter}")
        else:
            logger.info(f"You have not been faned!")

    return True


def save_content(content: str, path: str) -> bool:
    open(path, "w").write(content)
    return file_is_local(path)


def file_is_local(path: str) -> bool:
    return pathlib.Path(path).exists()


def dir_is_local(path: str) -> bool:
    return pathlib.Path(path).is_dir()


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
        "linktr.ee": [
            {"find": r"linktr.ee%2F[a-zA-Z_-]+", "post": urllib.parse.unquote},  # href={enconded_link}
            {"find": r"linktr.ee/[a-zA-Z_-]+", "post": ""}  # <span>{link}<span>,

        ],
        "beacons.ai": [
            {"find": r"beacons.ai%2F[a-zA-Z_-]+", "post": urllib.parse.unquote},  # href={enconded_link}
            {"find": r"beacons.ai/[a-zA-Z_-]+", "post": ""}  # <span>{link}<span>
        ],
        "lnk.bio": [
            {"find": r"lnk.bio%2F[a-zA-Z_-]+", "post": urllib.parse.unquote},
            {"find": r"lnk.bio/[a-zA-Z_-]+", "post": ""}
        ]
    }

    found_providers = []

    for provider, patterns in providers.items():

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
    content = ""
    for link in links:
        if "beacons" in link[0]:
            content = selenium_get_content(link[1], as_headless=False)

        if "linktr" in link[0]:
            content = requests_get_content(link[1])

        if "lnk" in link[0]:
            content = selenium_get_content(link[1], as_headless=False)

    return content


def has_onlyfans(content: str) -> dict:
    has = {}
    link = re.findall(r"https://onlyfans.com/[A-Za-z_-]+", content)

    if link:
        link = list(set(link))  # OF requests.get returns 2 links sometimes, deduplicate
        has["source"] = "onlyfans"
        has["url"] = link[0]

    return has


def has_fansly(content: str) -> str:
    pass


def has_twitter(url: str) -> str:
    pass
