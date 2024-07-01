from fastapi import FastAPI, File, Request, status
from typing import Annotated

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from creategif import CreateAsciiArt


app = FastAPI()

origins = ["http://localhost:8000","localhost:8000","https://web-ascii-arter.deno.dev/"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def handler(request: Request, exc: RequestValidationError):
    print(exc)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.post("/files/")
async def create_files(files: Annotated[bytes, File()]):
    output = CreateAsciiArt().create_ascii_art_from_binary(files)

    return Response(content=output, media_type="image/gif")
