from models import Provider

onlyfans_provider = Provider(
    name="onlyfans",
    link_finders=[
        {"find": r"onlyfans.com/[0-9A-Za-z_-]+", "post": ""},
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
