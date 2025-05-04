from dotenv import load_dotenv

from handler.auth_handler import AuthHandler
from handler.previous_day_study_handler import \
    record_previous_day_study_for_material

load_dotenv()

auth_handler = AuthHandler()
auth_res = auth_handler.auth()
print(f"認証成功: ユーザー名 {auth_res.username}")

study_record_res = record_previous_day_study_for_material(
    access_token=auth_res.access_token,
    username=auth_res.username,
    duration=3600,  # 1 hour
    comment="前日の勉強記録（自動的に23:59に設定）",
)

if study_record_res:
    print(f"前日の勉強記録を作成しました: {study_record_res}")
else:
    print("本棚に教材がありません。")
