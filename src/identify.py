from typing import Optional

from src.content import re_get_content
from src.content_providers.fans_providers import *
from src.content_providers.link_providers import *


def identify_link_provider(content: str) -> list[Optional[list]]:
    providers = [
        lnk_provider,
        lnktr_provider,
        allmylinks_provider,
        beacons_provider
    ]

    return re_get_content(providers, content)


def identify_fans_provider(content: str) -> list:
    fans_providers = [
        onlyfans_provider,
        fansly_provider,
        fanvue_provider
    ]

    return re_get_content(fans_providers, content)
