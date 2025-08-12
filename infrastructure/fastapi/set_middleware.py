from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware


def set_middleware(app):
    app.add_middleware(SessionMiddleware, secret_key="!secret")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://localhost:3000",  # ton front Next.js
            "https://127.0.0.1:3000",  # si tu utilises les deux
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
