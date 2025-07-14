import urllib

from src.models import Provider

lnktr_provider = Provider(
    name="linktree",
    link_finders=[
        {"find": r"linktr.ee%2F[0-9a-zA-Z_-]+", "post": urllib.parse.unquote},  # href={enconded_link}
        {"find": r"linktr.ee/[0-9a-zA-Z_-]+", "post": ""}  # <span>{link}<span>,
    ],
    exceptions=[])

beacons_provider = Provider(
    name="beacons",
    link_finders=[
        {"find": r"beacons.ai%2F[0-9a-zA-Z_-]+", "post": urllib.parse.unquote},
        {"find": r"beacons.ai/[0-9a-zA-Z_-]+", "post": ""}
    ],
    exceptions=[])

lnk_provider = Provider(
    name="lnk",
    link_finders=[
        {"find": r"lnk.bio%2F[0-9a-zA-Z_-]+", "post": urllib.parse.unquote},
        {"find": r"lnk.bio/[0-9a-zA-Z_-]+", "post": ""}
    ],
    exceptions=[])

allmylinks_provider = Provider(
    name="allmylinks",
    link_finders=[
        {"find": r"allmylinks.com%2F[0-9a-zA-Z_-]+", "post": urllib.parse.unquote},
        {"find": r"allmylinks.com/[0-9a-zA-Z_-]+", "post": ""}
    ],
    exceptions=[])