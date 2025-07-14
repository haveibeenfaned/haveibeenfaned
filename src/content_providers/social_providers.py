from models import Provider

instagram_provider = Provider(
    name="ig",
    link_finders=[],
    exceptions=[
        {"find": r">sorry, this page isn't available", "response": "IG Profile Not Found"},
        {"find": r">something went wrong",
         "response": "IG Profile Not Found due to Crawler being blocked, try again later"}
    ])