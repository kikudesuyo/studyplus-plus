from typing import Any, Dict, Optional

from pydantic import BaseModel


class StudyChallengePeriod(BaseModel):
    start_date: Optional[str]
    end_date: Optional[str]


class StudyChallenge(BaseModel):
    challenge_period: Optional[StudyChallengePeriod] = None
    challenge_duration: Optional[int] = None
    prev_duration: Optional[int] = None
    duration: Optional[int] = None
    prev_ratio: Optional[int] = None
    ratio: Optional[int] = None


class StudyRecordModel(BaseModel):
    record_id: int
    connection_result: Optional[Dict[str, Any]] = {}
    status: Optional[str] = ""
    study_challenge: Optional[StudyChallenge] = None
