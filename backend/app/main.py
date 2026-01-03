from fastapi import FastAPI

from app.core.config import settings
from app.core.startup import startup_event
from app.api.v1.router import api_router
from app.api.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        description="API para detecção de transações financeiras suspeitas.",
        version="1.0.0",
        debug=settings.DEBUG
    )

    # 🔥 STARTUP
    app.add_event_handler("startup", startup_event)

    # Rotas
    app.include_router(health_router)
    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
