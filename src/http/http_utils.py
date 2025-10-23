import os

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware


def create_cors_middleware() -> Middleware:
    allowed_origins = []
    avni_base_url = os.getenv("AVNI_BASE_URL")

    if avni_base_url:
        allowed_origins.append(avni_base_url)
    allowed_origins.extend(["http://localhost:6010"])

    return Middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )
