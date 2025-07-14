from dataclasses import dataclass
from typing import Optional, List, Dict

@dataclass(frozen=False)
class Profile:
    ig_url: str
    handle: str
    onlyfans_url: str = None
    fansly_url: str = None
    linktree_url: str = None
    beacons_url: str = None
    lnk_url: str = None
    allmylinks_url: str = None
    fanvue_url: str = None
    funny_page: bool = False


@dataclass(frozen=True)
class Provider:
    name: str
    link_finders: Optional[List]
    exceptions: List[Optional[Dict[str, str]]]
