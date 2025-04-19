import logging
import pathlib
import sys

from src.content import selenium_get_content, get_provider_content
from src.identify import identify_provider, identify_funny_content
from src.utils import file_is_local, save_content

logger = logging.getLogger("app-loger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
url = 'https://www.instagram.com/platinump_____/?hl=en'
logger.addHandler(handler)


# TODO: If no provider found -> return @s linked so you can input those instead on the front end
# TODO: Add search mode + append mode
# TODO: Add database integration
# TODO: Add tests
# TODO: Add base infra
# TODO: Add github actions for tests / base infra deployments


def app():
    # beacons / lik.bio / link.tree / allmylinks

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
        logger.warning("Page empty or does not exist")
        return False

    logger.info(f"Profile found: {url}")
    found_links = identify_provider(content)

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

        funny_content = identify_funny_content(funny_page)
        if funny_content:
            logger.info(f"You have been faned: {funny_content}, He/She is for the streets.")
        else:
            logger.info(f"You have not been faned! He/She is a keeper.")

    return True
