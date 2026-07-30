from fastapi import APIRouter

from app.routes.health_routes import router as health_router

ALL_ROUTERS: list[APIRouter] = [health_router]
