from studyplus.api.repository.auth import AuthRepository, AuthRepositoryRes


def get_auth() -> AuthRepositoryRes:
    """認証を取得する関数"""
    auth_repo = AuthRepository()
    return auth_repo.auth()
