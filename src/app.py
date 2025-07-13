import http.client
import logging
import sys
from typing import List, Union

from src.content import re_get_exceptions
from src.content import selenium_get_content, get_provider_content
from src.database import save_profile, notify_back
from src.identify import identify_link_provider, identify_fans_provider
from src.models import Profile
from src.providers import instagram_provider, Provider

logger = logging.getLogger(name="crawler")
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("crawler.log")

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


def app(handle: str = "lauramedinarb"):
    logger.info(f"Start crawling: {handle}")
    URL = f"https://www.instagram.com/{handle}"
    profile = Profile(handle=handle, ig_url=URL)
    response = {"exception": "", "isException": False, "profile": profile, "status_code": 200}

    content = selenium_get_content(URL, as_headless=False)
    if not content:
        logger.info(f"Crawler - No Data found: {URL}")
        return notify_back(
            create_payload(isException=True, exception="Crawler - Not Found Error ",
                           status_code=http.client.NOT_FOUND, **response))

    exception_response = re_get_exceptions([instagram_provider], content)
    if exception_response:
        logger.warning(exception_response)
        return notify_back(
            create_payload(isException=True, exception=exception_response, status_code=http.client.FAILED_DEPENDENCY,
                           **response))

    saved = save_profile(profile)
    if not saved:
        logger.warning(f"Database - Could not save profile: {profile}")
        return notify_back(create_payload(isException=True, exception="Database - Internal Server Error",
                                          status_code=http.client.INTERNAL_SERVER_ERROR, **response))

    logger.info(f"Crawler - Profile found and saved: {URL}")
    providers_links: List[List[Union[Provider, str]]] = identify_link_provider(content)
    fans_links = identify_fans_provider(content)

    for link in fans_links:
        logger.info(f"Crawler - Fans link found: {link}, appending to Profile")
        profile.__setattr__(f"{link[0]}_URL", link[1])

    saved = save_profile(profile)
    if not saved:
        logger.warning(f"Database - Could not save profile: {profile}")
        return notify_back(create_payload(isException=True, exception="Database - Internal Server Error",
                                          status_code=http.client.INTERNAL_SERVER_ERROR, **response))

    for link in providers_links:
        provider = link[0]
        profile.__setattr__(f"{provider.name}_URL", link[1])

    saved = save_profile(profile)
    if not saved:
        logger.warning(f"Database - Could not save profile: {profile}")
        return notify_back(create_payload(isException=True, exception="Database - Internal Server Error",
                                          status_code=http.client.INTERNAL_SERVER_ERROR, **response))

    for link in providers_links:
        provider = link[0]
        content = get_provider_content(link[1])

        if not content:
            logger.info(f"Crawler - No content found for link provider: {link}")
            res = {"exception": exception_response, "isException": True, "profile": profile.__dict__}
            return notify_back(
                create_payload(isException=True, exception="Crawler - No content found for link provider",
                               status_code=http.client.INTERNAL_SERVER_ERROR, **res))

        exception_response = re_get_exceptions([provider], content)

        if exception_response:
            logger.warning(exception_response)
            return notify_back(create_payload(isException=True, exception=exception_response,
                                              status_code=http.client.INTERNAL_SERVER_ERROR,
                                              **response))

        found_urls = identify_fans_provider(content)

        if not found_urls:
            logger.info(f"Crawler - No content found for link provider: {link}")

        for provider in found_urls:
            profile.funny_page = True
            profile.__setattr__(f"{provider[0].name}_URL", provider[1])

    print(f"Crawler - Finished Crawling: {handle}, saving profile and returning response")

    saved = save_profile(profile)
    if not saved:
        logger.warning(f"Database - Could not save profile: {profile}")
        return notify_back(create_payload(isException=True, exception="Database - Internal Server Error",
                                          status_code=http.client.INTERNAL_SERVER_ERROR, **response))

    if profile.funny_page:
        logger.info(f"You have been faned! He/She is for the streets.")
        return notify_back(create_payload(**response))
    else:
        logger.info(f"You have not been faned! He/She is a keeper.")
        return notify_back(create_payload(**response))


def create_payload(**kwargs) -> dict:
    return dict(**kwargs)
