import argparse
from dotenv import load_dotenv

from handler.auth_handler import AuthHandler
from handler.bookshelf_entries_handler import BookshelfEntriesHandler
from handler.me_handler import MeHandler
from handler.study_records_handler import StudyRecordsHandler
from handler.like_handler import LikeHandler

def main():
    parser = argparse.ArgumentParser(description="Studyplus CLI")
    subparsers = parser.add_subparsers(dest="command", help="コマンド")

    parser.add_argument("--me", action="store_true", help="ユーザー情報を取得")

    parser.add_argument("--bookshelf", action="store_true", help="本棚エントリーを取得")

    study_parser = subparsers.add_parser("study", help="勉強記録を作成")
    study_parser.add_argument("--material", required=True, help="教材コード")
    study_parser.add_argument("--duration", type=int, required=True, help="勉強時間（秒）")
    study_parser.add_argument("--comment", help="コメント")

    like_parser = subparsers.add_parser("like", help="投稿にいいねする")
    like_parser.add_argument("--username", required=True, help="いいねするユーザー名")
    like_parser.add_argument("--count", type=int, default=5, help="いいねする投稿数（デフォルト: 5）")

    args = parser.parse_args()

    load_dotenv()

    auth_handler = AuthHandler()
    auth_res = auth_handler.auth()
    print(f"認証成功: ユーザー名 {auth_res.username}")

    if args.command is None:
        if args.me:
            me_handler = MeHandler(auth_res.access_token)
            me = me_handler.get_me()
            print(f"ユーザー情報: {me}")
        
        elif args.bookshelf:
            bookshelf_entries_handler = BookshelfEntriesHandler(
                auth_res.access_token, auth_res.username
            )
            bookshelf_entries_res = bookshelf_entries_handler.get_bookshelf_entries()
            print(f"本棚エントリー: {bookshelf_entries_res}")
        
        else:
            parser.print_help()
    
    elif args.command == "study":
        study_records_handler = StudyRecordsHandler(auth_res.access_token)
        study_records_res = study_records_handler.create_study_record(
            material_code=args.material,
            duration=args.duration,
            comment=args.comment,
        )
        print(f"勉強記録作成: {study_records_res}")
    
    elif args.command == "like":
        like_handler = LikeHandler(auth_res.access_token)
        print(f"{args.username}の最新{args.count}件の投稿にいいねします...")
        results = like_handler.like_user_latest_posts(args.username, args.count)
        
        success_count = sum(1 for result in results if result.success)
        print(f"いいね完了: {success_count}/{len(results)}件")
        
        for i, result in enumerate(results):
            if not result.success and result.message:
                print(f"投稿 {i+1}: {result.message}")

if __name__ == "__main__":
    main()
