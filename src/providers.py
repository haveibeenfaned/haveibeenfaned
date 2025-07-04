import urllib

from src.models import Provider

lnktr_provider = Provider(
    name="lnktree",
    link_finders=[
        {"find": r"linktr.ee%2F[a-zA-Z_-]+", "post": urllib.parse.unquote},  # href={enconded_link}
        {"find": r"linktr.ee/[a-zA-Z_-]+", "post": ""}  # <span>{link}<span>,
    ],
    exceptions=[])

beacons_provider = Provider(
    name="beacons",
    link_finders=[
        {"find": r"beacons.ai%2F[a-zA-Z_-]+", "post": urllib.parse.unquote},
        {"find": r"beacons.ai/[a-zA-Z_-]+", "post": ""}
    ],
    exceptions=[])

lnk_provider = Provider(
    name="lnk",
    link_finders=[
        {"find": r"lnk.bio%2F[a-zA-Z_-]+", "post": urllib.parse.unquote},
        {"find": r"lnk.bio/[a-zA-Z_-]+", "post": ""}
    ],
    exceptions=[])

allmylinks_provider = Provider(
    name="allmylinks",
    link_finders=[
        {"find": r"allmylinks.com%2F[a-zA-Z_-]+", "post": urllib.parse.unquote},
        {"find": r"allmylinks.com/[a-zA-Z_-]+", "post": ""}
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
        {"find": r"onlyfans.com/[A-Za-z_-]+", "post": ""}
    ],
    exceptions=[]
)

fansly_provider = Provider(
    name="fansly",
    link_finders=[
        {"find": r"fansly.com/[A-Za-z_-]+", "post": ""}
    ],
    exceptions=[]
)
