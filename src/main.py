from dotenv import load_dotenv

from handler.auth_handler import AuthHandler
from handler.bookshelf_entries_handler import BookshelfEntriesHandler
from handler.me_handler import get_me
from handler.study_records_handler import StudyRecordsHandler

load_dotenv()

auth_handler = AuthHandler()
auth_res = auth_handler.auth()

# me = get_me(auth_res.access_token)
# bookshelf_entries_handler = BookshelfEntriesHandler(
#     auth_res.access_token, auth_res.username
# )
# bookshelf_entries_res = bookshelf_entries_handler.get_bookshelf_entries()
# print(bookshelf_entries_res)

study_records_handler = StudyRecordsHandler(auth_res.access_token)
study_records_res = study_records_handler.create_study_record(
    material_code="ASIN4861103525",
    duration=36000,
    comment="頑張ったゔぃん",
)
print(study_records_res)
