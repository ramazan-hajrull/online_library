import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pathlib import Path
import uvicorn
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

sys.path.append(str(Path(__file__).parent.parent))

from src.init import redis_manager

from src.api.auth import router as router_auth
from src.api.users import router as router_users
from src.api.authors import router as router_authors
from src.api.books import router as router_books
from src.api.reviews import router as router_reviews
from src.api.favorites import router as router_favorites
from src.api.admin import router as router_admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis),
prefix="fastapi-cache")
    yield
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def force_revalidate_cache(request, call_next):
    response = await call_next(request)
    if "cache-control" in response.headers:
        response.headers["Cache-Control"] = "no-cache"
    return response

app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_authors)
app.include_router(router_books)
app.include_router(router_reviews)
app.include_router(router_favorites)
app.include_router(router_admin)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
