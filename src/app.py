import json
import logging
import os
import pathlib
import sys
from typing import List, Union

import psycopg

from src.content import re_get_exceptions
from src.content import selenium_get_content, get_provider_content
from src.database import save_profile
from src.identify import identify_provider, identify_funny_content
from src.models import Profile
from src.providers import instagram_provider, Provider
from src.utils import file_is_local

logger = logging.getLogger(name="crawler")
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("crawler.log")

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

host = os.getenv("DB_HOST", "localhost")
dbname = os.getenv("DB_NAME", "postgres")
user = os.getenv("DB_USER", "postgres")
password = os.getenv("DB_PASSWORD", "1234")


def app(handle: str = "lauramedinarb"):
    # beacons / lik.bio / link.tree / allmylinks
    print(f"Start crawling: {handle}")
    url = f"https://www.instagram.com/{handle}"
    username = url.strip().split("/")[3].lower()
    fname = f"{username}.txt"
    content = selenium_get_content(url, as_headless=False)
    exception_response = re_get_exceptions([instagram_provider], content)

    if exception_response:
        logger.warning(exception_response)
        res = {"exception": exception_response, "isException": True, "profile": {}}
        return notify_back(res)

    profile = Profile(
        ig_url=url,
        handle=username,
        fname=fname
    )
    saved = save_profile(profile)
    if not saved:
        logger.error("Could not save profile in DB, bad news")
        res = {"exception": "Internal Database Error", "isException": True, "profile": profile.__dict__}
        return notify_back(res)


    # TODO: Add if error idiom in the two following lines
    logger.info(f"Profile found and saved: {url}")
    found_links: List[List[Union[Provider, str]]] = identify_provider(content)
    funny_content = identify_funny_content(content)

    for link in funny_content:
        logger.info(f"Funny content found: {link}, appending to Profile")
        profile.__setattr__(f"{link[0]}_url", link[1])

    for link in found_links:
        provider = link[0]
        profile.__setattr__(f"{provider.name}_url", link[1])

        funny_page = get_provider_content(link[1])
        exception_response = re_get_exceptions([provider], funny_page)
        if not funny_page or exception_response:
            logger.info("No content found in funny provider link, strange")
            res = {"exception": exception_response, "isException": True, "profile": profile.__dict__}
            return notify_back(res)

        if funny_page:
            found_urls = identify_funny_content(funny_page)
            for provider in found_urls:
                profile.funny_page = True
                profile.__setattr__(f"{provider[0].name}_url", provider[1])

    print(f"Finished crawling: {handle}, returning response asap")

    res = save_profile(profile)
    if not res:
        logger.error("Could not save profile in DB, bad news")
        res = {"exception": "Internal Database Error", "isException": True, "profile": profile.__dict__}
        return notify_back(res)

    if profile.funny_page:
        res = {"exception": exception_response, "isException": False, "profile": profile.__dict__}
        logger.info(f"You have been faned! He/She is for the streets.")
        return notify_back(res)
    else:
        res = {"exception": exception_response, "isException": False, "profile": profile.__dict__}
        logger.info(f"You have not been faned! He/She is a keeper.")
        return notify_back(res)


def notify_back(res: dict) -> bool:
    with psycopg.connect(host=host, dbname=dbname, user=user, password=password) as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"NOTIFY responses, '{json.dumps(res)}'")
        connection.commit()
    return True
