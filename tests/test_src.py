import pathlib
import urllib

from src.content import requests_get_content, as_headless
from src.content import selenium_get_content
from src.content import re_get_content
from src.content import get_provider_content

from selenium import webdriver

test_directory = "/tests"
abs_path = str(pathlib.Path().absolute())
data_path = str(pathlib.Path().absolute())[0:abs_path.index(test_directory)+len(test_directory) ] + "/testdata"

def test_requests_get_content():
    # lnktr.ee

    url = "https://linktr.ee/Laceye"  # profiles/linktr_ee/onlyfans_linktree.txt
    res = requests_get_content(url)

    assert res is not None

    url = "https://linktr.ee/jgwerihdsbk"  # gibberish gets 404
    res = requests_get_content(url)

    assert not res


def test_selenium_get_content():
    # instagram existing
    url = "https://www.instagram.com/platinump_____/?hl=en"
    res = selenium_get_content(url)
    assert res

    # instagram non existant
    url = "https://www.instagram.com/fewjouihgfewhos/?hl=en"
    res = selenium_get_content(url)
    assert not res

    # beacons.ai
    url = "https://www.instagram.com/theoriisworld/?hl=en"
    res = selenium_get_content(url)
    assert res

    # lnk.bio
    url = "https://www.instagram.com/msjennafischer/?hl=en"
    res = selenium_get_content(url)
    assert res

    # allmylinks.com TBD
    url = "https://www.instagram.com/platinump_____/?hl=en"
    res = selenium_get_content(url)
    assert res


def test_as_headless():
    options = as_headless(webdriver.ChromeOptions())

    assert "--headless=new" in options.arguments


def test_get_provider_content():
    urls = [
        ["beacons.ai", "https://www.instagram.com/platinump_____/?hl=en"],
        ["linktr", "https://www.instagram.com/theoriisworld/?hl=en"],
        ["lnk", "https://www.instagram.com/msjennafischer/?hl=en"],
        ["allmylinks", "https://www.instagram.com/platinump_____/?hl=en"]
    ]

    content = []
    for url in urls:
        content.append(get_provider_content([url]))

    assert len(content) == len(urls)


def test_re_get_content():
    # complex testing since it requires other functions to function hehe
    # src.identify.identify_funny_content + onlyfans

    content_provider = {
        "onlyfans": [
            {"find": r"onlyfans.com/[A-Za-z_-]+", "post": ""}
        ],
        "fansly": [
            {"find": r"fansly.com/[A-Za-z_-]+", "post": ""}
        ]
    }

    # src.identify.identify_funny_content + fansly

    content_provider = {
        "onlyfans": [
            {"find": r"onlyfans.com/[A-Za-z_-]+", "post": ""}
        ],
        "fansly": [
            {"find": r"fansly.com/[A-Za-z_-]+", "post": ""}
        ]
    }

    # src.identify.idenfity_funny_content_no_provider

    content_provider = {
        "onlyfans": [
            {"find": r"onlyfans.com/[A-Za-z_-]+", "post": ""}
        ],
        "fansly": [
            {"find": r"fansly.com/[A-Za-z_-]+", "post": ""}
        ]
    }

    # src.identify.identify_provider

    providers = {
        "linktr.ee": [
            {"find": r"linktr.ee%2F[a-zA-Z_-]+", "post": urllib.parse.unquote},  # href={enconded_link}
            {"find": r"linktr.ee/[a-zA-Z_-]+", "post": ""}  # <span>{link}<span>,
        ],
        "beacons.ai": [
            {"find": r"beacons.ai%2F[a-zA-Z_-]+", "post": urllib.parse.unquote},
            {"find": r"beacons.ai/[a-zA-Z_-]+", "post": ""}
        ],
        "lnk.bio": [
            {"find": r"lnk.bio%2F[a-zA-Z_-]+", "post": urllib.parse.unquote},
            {"find": r"lnk.bio/[a-zA-Z_-]+", "post": ""}
        ],
        "allmylinks.com": [
            {"find": r"allmylinks.com%2F[a-zA-Z_-]+", "post": urllib.parse.unquote},
            {"find": r"allmylinks.com/[a-zA-Z_-]+", "post": ""}
        ]
    }

    # linktr
    content = open(f"{data_path}/profiles/linktr/limitlessmacey.txt").read()
    res = re_get_content(content_provider, content)



    assert res is not None

