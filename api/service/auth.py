from api.external.studyplus.auth import Auth, AuthReq
from api.model.auth_model import AuthModel


def auth(consumer_key, consumer_secret, email, pasword) -> AuthModel:
    payload = AuthReq(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        password=pasword,
        username=email,
    )

    res = Auth().auth(payload)
    return AuthModel(
        access_token=res.access_token,
        refresh_token=res.refresh_token,
        studyplus_user_id=res.username,
    )
