import os
from typing import Optional


def get_required_env_var(name: str) -> str:
    """環境変数を取得し、存在しない場合はエラーを発生させる"""
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} must be set in the environment variables.")
    return value


def get_optional_env_var(name: str, default: Optional[str] = None) -> Optional[str]:
    """環境変数を取得し、存在しない場合はデフォルト値を返す"""
    return os.getenv(name, default)
