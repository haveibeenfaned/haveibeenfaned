import http.client
import logging
import os
import pathlib
import sys
from typing import List, Union

from src.content import re_get_exceptions
from src.content import selenium_get_content, get_provider_content
from src.content_providers.social_providers import instagram_provider
from src.database import save_profile, notify_back, profile_exists
from src.identify import identify_link_provider, identify_fans_provider
from src.models import Profile, Provider

logger = logging.getLogger(name="crawler")
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("crawler.log")

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


def app(handle: str = "lauramedinarb"):
    logger.info(f"Crawler - Start crawling: {handle}")
    URL = f"https://www.instagram.com/{handle}"

    profile = profile_exists(handle)

    if profile and profile.funny_page:
        logger.info(f"Crawler - Profile exists and has already been shamed: {handle}")
        return notify_back(
            create_payload(isException=False, exception="Crawler - Already Crawled and Shamed",
                           status_code=http.client.OK, profile=profile))

    # Override profile if it already exists and needs recrawling
    profile = Profile(handle=handle, ig_url=URL)

    logger.info(f"Crawler - Getting Selenium Content")
    content = selenium_get_content(URL, profile=handle, as_headless=False)
    if not content:
        logger.info(f"Crawler - No Data found: {URL}")
        return notify_back(
            create_payload(isException=True, exception="Crawler - Not Found Error ",
                           status_code=http.client.NOT_FOUND, profile=profile))

    logger.info(f"Crawler - Analysing Exceptions")
    exception_response = re_get_exceptions([instagram_provider], content)
    if exception_response:
        logger.warning(exception_response)
        return notify_back(
            create_payload(isException=True, exception=exception_response,
                           status_code=http.client.FAILED_DEPENDENCY, profile=profile))

    logger.info(f"Crawler - Saving Profile")
    saved = save_profile(profile)
    if not saved:
        logger.warning(f"Database - Could not save profile: {profile}")
        return notify_back(create_payload(isException=True, exception="Database - Internal Server Error",
                                          status_code=http.client.INTERNAL_SERVER_ERROR, profile=profile))

    logger.info(f"Crawler - Profile found and saved: {URL}")
    providers_links: List[List[Union[Provider, str]]] = identify_link_provider(content)
    fans_links = identify_fans_provider(content)

    for link in fans_links:
        logger.info(f"Crawler - Fans link found: {link}, appending to Profile")
        profile.__setattr__(f"{link[0]}_url", link[1])

    saved = save_profile(profile)
    if not saved:
        logger.warning(f"Database - Could not save profile: {profile}")
        return notify_back(create_payload(isException=True, exception="Database - Internal Server Error",
                                          status_code=http.client.INTERNAL_SERVER_ERROR, profile=profile))

    for link in providers_links:
        provider = link[0]
        profile.__setattr__(f"{provider.name}_url", link[1])

    saved = save_profile(profile)
    if not saved:
        logger.warning(f"Database - Could not save profile: {profile}")
        return notify_back(create_payload(isException=True, exception="Database - Internal Server Error",
                                          status_code=http.client.INTERNAL_SERVER_ERROR, profile=profile))

    for link in providers_links:
        provider = link[0]
        content = get_provider_content(link[1])

        if not content:
            logger.info(f"Crawler - No content found for link provider: {link}")
            return notify_back(
                create_payload(isException=True, exception="Crawler - No content found for link provider",
                               status_code=http.client.NOT_FOUND, profile=profile))

        exception_response = re_get_exceptions([provider], content)

        if exception_response:
            logger.warning(exception_response)
            return notify_back(create_payload(isException=True, exception=exception_response,
                                              status_code=http.client.NOT_FOUND, profile=profile))

        found_urls = identify_fans_provider(content)

        if not found_urls:
            logger.info(f"Crawler - No content found for link provider: {link}")

        for provider in found_urls:
            profile.funny_page = True
            profile.__setattr__(f"{provider[0].name}_url", provider[1])

    print(f"Crawler - Finished Crawling: {handle}, saving profile and returning response")

    saved = save_profile(profile)
    if not saved:
        logger.warning(f"Database - Could not save profile: {profile}")
        return notify_back(create_payload(isException=True, exception="Database - Internal Server Error",
                                          status_code=http.client.INTERNAL_SERVER_ERROR, profile=profile))

    if profile.funny_page:
        logger.info(f"You have been faned! He/She is for the streets.")
        return notify_back(create_payload(isException=False, exception="You have been faned! He/She is for the streets",
                                          status_code=http.client.OK, profile=profile))
    else:
        logger.info(f"You have not been faned! He/She is a keeper.")
        return notify_back(create_payload(isException=False, exception="You have NOT been faned! He/She is for the streets",
                                          status_code=http.client.OK, profile=profile))


def create_payload(**kwargs) -> dict:
    return dict(**kwargs)
