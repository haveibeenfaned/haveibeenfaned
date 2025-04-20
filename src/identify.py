import urllib
from typing import Optional

from src.content import re_get_content


def identify_provider(content: str) -> list[Optional[list]]:
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

    return re_get_content(providers, content)


def identify_funny_content_no_provider(content: str) -> list:
    content_provider = {
        "onlyfans": [
            {"find": r"https://onlyfans.com/[A-Za-z_-]+", "post": ""}
        ],
        "fansly": [
            {"find": r"https://fansly.com/[A-Za-z_-]+", "post": ""}
        ]
    }
    return re_get_content(content_provider, content)


def identify_funny_content(content: str) -> list:
    content_provider = {
        "onlyfans": [
            {"find": r"https://onlyfans.com/[A-Za-z_-]+", "post": ""}
        ],
        "fansly": [
            {"find": r"https://fansly.com/[A-Za-z_-]+", "post": ""}
        ]
    }

    return re_get_content(content_provider, content)
