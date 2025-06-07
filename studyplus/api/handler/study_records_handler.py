from studyplus.api.repository.study_records import (
    StudyRecordRepositoryRes,
    StudyRecordsRepository,
)


def create_study_record(
    access_token: str,
    material_code: str,
    duration: int,
    comment: str,
    post_token: str,
    record_datetime: str,
) -> StudyRecordRepositoryRes:
    """
    勉強記録を作成する関数

    Args:
        access_token: アクセストークン
        material_code: 教材ID
        duration: 勉強時間（秒）
        comment: コメント（オプション）
        post_token: ポストトークン（UUIDで生成）
        record_datetime: 記録日時（指定されない場合は現在時刻）

    Returns:
        StudyRecordRepositoryRes: APIレスポンス
    """
    study_records_repo = StudyRecordsRepository(access_token)
    return study_records_repo.create_study_record(
        material_code=material_code,
        duration=duration,
        comment=comment,
        post_token=post_token,
        record_datetime=record_datetime,
    )
