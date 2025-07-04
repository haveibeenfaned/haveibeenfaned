from typing import Optional

from src.content import re_get_content
from src.providers import *


def identify_provider(content: str) -> list[Optional[list]]:
    providers = [
        lnk_provider,
        lnktr_provider,
        allmylinks_provider,
        beacons_provider
    ]

    return re_get_content(providers, content)


def identify_funny_content(content: str) -> list:
    content_providers = [
        onlyfans_provider,
        fansly_provider
    ]

    return re_get_content(content_providers, content)
