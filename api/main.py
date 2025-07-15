from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from api.routes import r
from api.utils.error_reporter import ErrorReporter

load_dotenv()

app = FastAPI()


# Exception handler to report errors
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    ErrorReporter.report_exception(request, exc)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(r)
