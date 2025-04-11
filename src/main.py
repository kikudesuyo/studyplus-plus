import os

from dotenv import load_dotenv
from handler.auth_handler import AuthReq, auth
from handler.me_handler import get_me

load_dotenv()

email = os.getenv("STUDYPLUS_EMAIL")
if not email:
    raise ValueError("STUDYPLUS_EMAIL must be set in the environment variables.")
password = os.getenv("STUDYPLUS_PASSWORD")
if not password:
    raise ValueError("STUDYPLUS_PASSWORD must be set in the environment variables.")
consumer_key = os.getenv("CONSUMER_KEY")
if not consumer_key:
    raise ValueError("CONSUMER_KEY must be set in the environment variables.")
consumer_secret = os.getenv("CONSUMER_SECRET")
if not consumer_key or not consumer_secret:
    raise ValueError(
        "CONSUMER_KEY and CONSUMER_SECRET must be set in the environment variables."
    )

auth_req = AuthReq(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    password=password,
    username=email,
)
auth_res = auth(auth_req)

me = get_me(auth_res.access_token)
print(me)
