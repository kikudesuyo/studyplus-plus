from datetime import datetime
from typing import List

from api.external.gemini.client import generate_content_with_gemini
from api.service.weekly_study_battle.model import PlaceModel


def generate_comment(
    start: datetime,
    end: datetime,
    user_places: List[PlaceModel],
) -> str:
    """週間学習バトルの結果をコメントとして生成する"""
    sorted_user_places = sorted(user_places, key=lambda x: x.place)
    place_comments = []
    for place in sorted_user_places:
        hours = place.total_duration // 3600
        minutes = (place.total_duration % 3600) // 60
        place_comments.append(
            f"{place.place}位: {place.user.name}さん : {hours}時間{minutes}分"
        )
    place_comment = "\n".join(place_comments)

    return (
        f"📣勉強時間バトル {start.strftime('%Y-%m-%d')} ~ {end.strftime('%Y-%m-%d')} の結果です📣\n\n"
        + f"{place_comment}\n\n"
        + f"勝者は {sorted_user_places[0].user.name} さんです！おめでとうございます🎉\n"
        + __generate_result_summary(sorted_user_places)
        + f"次回も頑張りましょう！🔥\n"
        + f"See you next week ;D"
    )


def __generate_result_summary(user_places: List[PlaceModel]) -> str:
    prompt = f"""
    あなたは勉強時間バトルの結果を要約し、感情的でポジティブなトーンでコメントを生成してください。
    出力は「はい、わかりました」や「以下が結果です」などの前置きや説明を一切含めず、直接コメント本文のみを出力してください。
    
    ユーザー名:miyavin 
    一人称は「miyavin」を使用してください。
    使用する場合は、いずれかの一人称を選び、統一してください。

    勉強時間バトルの結果は、ユーザー名、順位、勉強時間を含むデータです。勉強時間は秒で与えられるため、もし勉強時間について言及する場合は、時間と分に変換してから言及してください。
    以下のデータは、1週間の勉強時間のランキングです。
    データ:
    {user_places}
    ユーザー名、順位、勉強時間をもとに、以下の条件に従ってコメントを生成してください。
    条件:
    1. コメントは日本語で書いてください。
    2. 結果を基に要約してください。
    3. 勝者を中心に、他のユーザーの努力も称える内容にしてください。
    4. コメントは感情的で、ポジティブなトーンで書いてください。
    5. あなたが勉強をするわけではないので「見習って、私も頑張る」といった表現は使用しないでください。あくまでも他者を称える内容にしてください。
    6. 勉強時間について言及する場合は、時間と分に変換してから言及してください。
    7. 他者に比べて圧倒的に勉強時間が優れている場合は、その点を強調して褒め称えてください。
    8. 他者に比べて圧倒的に勉強時間が劣っている場合は、少しだけ煽るような内容にしてください。ユーモアのある煽りをするとより良いです。    
    9. 最後に次回の勉強時間バトルへの期待感を表現してください。
    10. 各ユーザーのコメントは1~2文程度にしてください。
    11. 前置きや説明文は一切書かず、コメント本文のみを出力してください。
    """
    return generate_content_with_gemini(
        prompt=prompt,
    )
