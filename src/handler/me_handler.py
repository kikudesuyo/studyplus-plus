import requests


def get_me(access_token: str):
    url = "https://api.studyplus.jp/2/me"
    headers = {
        "Authorization": f"OAuth {access_token}",
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ja",
        "Client-Service": "Studyplus",
        "Origin": "https://app.studyplus.jp",
        "Referer": "https://app.studyplus.jp/",
        "Sec-CH-UA": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"macOS"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Stpl-Client-Sp2": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Failed to fetch user info: {response.status_code} - {response.text}"
        )
