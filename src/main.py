from dotenv import load_dotenv
from handler.auth_handler import AuthHandler
from handler.me_handler import MeHandler
from handler.bookshelf_entries_handler import BookshelfEntriesHandler

load_dotenv()

auth_handler = AuthHandler()
auth_res = auth_handler.auth()
print(f"認証成功: ユーザー名 {auth_res.username}")

me_handler = MeHandler(auth_res.access_token)
me = me_handler.get_me()
print(f"ユーザー情報: {me}")

bookshelf_entries_handler = BookshelfEntriesHandler(auth_res.access_token, auth_res.username)
bookshelf_entries_res = bookshelf_entries_handler.get_bookshelf_entries()
print(f"本棚エントリー: {bookshelf_entries_res}")
