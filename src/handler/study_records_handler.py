import uuid
from datetime import datetime
from typing import Any, Dict, Optional

import requests
from pydantic import BaseModel, ConfigDict, Field


class StudyRecordReq(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    material_code: str = Field(..., alias="material_code")
    duration: int = Field(..., alias="duration")
    post_token: str = Field(..., alias="post_token")
    record_datetime: str = Field(..., alias="record_datetime")
    comment: Optional[str] = Field(None, alias="comment")
    runtimeType: str = Field("default", alias="runtimeType")
    study_source_type: str = Field("studyplus", alias="study_source_type")


class StudyChallengePeriod(BaseModel):
    start_date: str
    end_date: str


class StudyChallenge(BaseModel):
    challenge_period: StudyChallengePeriod
    challenge_duration: int
    prev_duration: int
    duration: int
    prev_ratio: int
    ratio: int


class StudyRecordRes(BaseModel):
    record_id: int
    connection_result: Dict[str, Any] = {}
    status: str = ""
    study_challenge: Optional[StudyChallenge] = None


class StudyRecordsHandler:
    def __init__(self, access_token: str):
        self.access_token = access_token

    def _generate_post_token(self) -> str:
        """
        UUIDを生成して文字列形式で返します。
        例: "7160a019-d73b-483b-ad75-3f9e850ea9e6"
        """
        return str(uuid.uuid4())

    def _get_current_datetime_iso(self) -> str:
        """
        現在の日時をISO形式で返します。
        例: "2025-05-03T23:31:37.623+09:00"
        """
        now = datetime.now().astimezone()
        return now.isoformat()

    def create_study_record(
        self,
        material_code: str,
        duration: int,
        comment: Optional[str] = None,
        post_token: Optional[str] = None,
        record_datetime: Optional[str] = None,
    ) -> StudyRecordRes:
        """
        勉強記録を作成します。

        Args:
            material_code: 教材ID
            duration: 勉強時間（秒）
            comment: コメント（オプション）
            post_token: ポストトークン（指定されない場合は自動生成）
            record_datetime: 記録日時（指定されない場合は現在時刻）

        Returns:
            StudyRecordRes: APIレスポンス
        """
        if not post_token:
            post_token = self._generate_post_token()

        if not record_datetime:
            record_datetime = self._get_current_datetime_iso()

        req = StudyRecordReq(
            material_code=material_code,
            duration=duration,
            post_token=post_token,
            record_datetime=record_datetime,
            comment=comment,
        )

        url = "https://api.studyplus.jp/2/study_records"
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "authorization": f"OAuth {self.access_token}",
            "client-service": "Studyplus",
            "content-type": "application/json; charset=utf-8",
            "origin": "https://app.studyplus.jp",
            "referer": "https://app.studyplus.jp/",
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "stpl-client-sp2": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        }

        payload = {
            "material_code": req.material_code,
            "duration": req.duration,
            "post_token": req.post_token,
            "record_datetime": req.record_datetime,
            "runtimeType": req.runtimeType,
            "study_source_type": req.study_source_type,
        }

        if req.comment:
            payload["comment"] = req.comment

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return StudyRecordRes(**response.json())
        else:
            raise Exception(
                f"Failed to create study record: {response.status_code} - {response.text}"
            )
