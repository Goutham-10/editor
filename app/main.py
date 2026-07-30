from fastapi import FastAPI

from app.logging_config import configure_logging
from app.routes import ALL_ROUTERS

configure_logging()

app = FastAPI(title="editor")

for router in ALL_ROUTERS:
    app.include_router(router)
