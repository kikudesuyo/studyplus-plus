from dotenv import load_dotenv
from handler.auth_handler import AuthHandler
from handler.me_handler import get_me

load_dotenv()

auth_handler = AuthHandler()
auth_res = auth_handler.auth()

me = get_me(auth_res.access_token)
print(me)
