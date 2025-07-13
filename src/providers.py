import urllib

from src.models import Provider

# TODO: add and test snipfeed.co

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

instagram_provider = Provider(
    name="ig",
    link_finders=[],
    exceptions=[
        {"find": r">sorry, this page isn't available", "response": "IG Profile Not Found"},
        {"find": r">something went wrong",
         "response": "IG Profile Not Found due to Crawler being blocked, try again later"}
    ])

onlyfans_provider = Provider(
    name="onlyfans",
    link_finders=[
        {"find": r"onlyfans.com/0-9[A-Za-z_-]+", "post": ""},
        {"find": r"onlyfans", "post": lambda x: f"https://{str(x)}.com/COULDNOTGETLINK"}
    ],
    exceptions=[]
)

fansly_provider = Provider(
    name="fansly",
    link_finders=[
        {"find": r"fansly.com/[0-9A-Za-z_-]+", "post": ""}
    ],
    exceptions=[]
)

fanvue_provider = Provider(
    name="fanvue",
    link_finders=[
        {"find": r"fanvue.com/[0-9A-Za-z_-]+", "post": ""}
    ],
    exceptions=[]
)
