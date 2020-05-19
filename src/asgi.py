"""
"""
from .routes import api_v1, token_router
from .core.config import settings
from .core.database import Base, engine
from .main import create_app

Base.metadata.create_all(bind=engine)
app = create_app()
app.include_router(api_v1, prefix=f"{settings.API_VERSION_PREFIX}")
app.include_router(token_router, prefix="/api/token", tags=["auth"])
