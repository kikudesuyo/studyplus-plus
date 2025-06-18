from external.studyplus.auth import Auth, AuthReq
from model.auth_model import AuthModel


def auth(consumer_key, consumer_secret, email, pasword) -> AuthModel:
    payload = AuthReq(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        password=pasword,
        username=email,
    )
    auth_repo = Auth()
    return auth_repo.auth(payload)
