import logging
import pathlib
import sys
import time
from typing import List, Union

from src.database import save_profile
from src.models import Profile
from src.content import re_get_exceptions
from src.content import selenium_get_content, get_provider_content
from src.identify import identify_provider, identify_funny_content
from src.providers import instagram_provider, Provider
from src.utils import file_is_local, save_content

logger = logging.getLogger(name="crawler")
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("crawler.log")

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


def app(url: str = "https://www.instagram.com/platinump____"):
    # beacons / lik.bio / link.tree / allmylinks

    username = url.strip().split("/")[3].lower()
    profiles_path = str(pathlib.Path().absolute()) + "/.data/profiles/"
    fname = f"{username}.txt"
    profile_file_path = profiles_path + fname

    # make sure it's saved for testing purposes because IG blocks it otherwise
    if file_is_local(profile_file_path):
        content = open(profile_file_path, "r").read()
        exception_response = re_get_exceptions([instagram_provider], content)
    else:
        content = selenium_get_content(url, as_headless=False)
        exception_response = re_get_exceptions([instagram_provider], content)

    if exception_response:
        logger.warning(exception_response)
        return exception_response

    saved = save_content(content, profile_file_path)
    profile = Profile(
        ig_url=url,
        handle=username,
        fname=fname
    )

    if not saved:
        logger.error("Error saving profile")
        return "Error saving profile, please try again later"

    logger.info(f"Profile found and saved: {url}")
    found_links: List[List[Union[Provider, str]]] = identify_provider(content)
    funny_content = identify_funny_content(content)

    for link in funny_content:
        logger.info(f"Funny content found: {link}, appending to Profile")
        profile.__setattr__(f"{link[0]}_url", link[1])

    for link in found_links:
        provider = link[0]
        profile.__setattr__(f"{provider.name}_url", link[1])
        profile_funny_page_file_path = profiles_path + f"{username}-{provider.name}.txt"

        if not file_is_local(profile_funny_page_file_path):
            funny_page = get_provider_content(link[1])
            exception_response = re_get_exceptions([provider], funny_page)
            if not funny_page or exception_response:
                logger.info("No content found in funny provider link, strange")
                return {"exception": exception_response, "isException": True, "profile": profile.__dict__}

            c = save_content(funny_page, profile_funny_page_file_path)
            if not c:
                logger.error("Could not save funny provider page")
                return {"exception": "Internal Server Error", "isException": True, "profile": profile.__dict__}
        else:
            funny_page = open(profile_funny_page_file_path, "r").read()

        if funny_page:
            found_urls = identify_funny_content(funny_page)
            for provider in found_urls:
                profile.funny_page = True
                profile.__setattr__(f"{provider[0].name}_url", provider[1])

    res = save_profile(profile)
    if not res:
        logger.error("Could not save profile in DB, bad news")
        return {"exception": "Internal Database Error", "isException": True, "profile": profile.__dict__}

    if profile.funny_page:
        response = {"exception": exception_response, "isException": False, "profile": profile.__dict__}
        logger.info(f"You have been faned! He/She is for the streets.")
    else:
        response = {"exception": exception_response, "isException": False, "profile": profile.__dict__}
        logger.info(f"You have not been faned! He/She is a keeper.")

    return response


def generate_consumption(postgres_conn):
    yield postgres_conn.poll()
    time.sleep(3)