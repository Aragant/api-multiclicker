from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware


def set_middleware(app):
    app.add_middleware(SessionMiddleware, secret_key="!secret")
    app.add_middleware(
        CORSMiddleware,allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
    )