from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass(frozen=False)
class Profile:
    ig_url: str
    handle: str
    onlyfans_url: str = ""
    fasnly_url: str = ""
    lnktree_url: str = ""
    beacons_url: str = ""
    lnk_url: str = ""
    allmylinks_url: str = ""
    fname: str = ""
    funny_page: bool = False


@dataclass(frozen=True)
class Provider:
    name: str
    link_finders: Optional[List]
    exceptions: List[Optional[Dict[str, str]]]
