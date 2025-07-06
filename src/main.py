from contextlib import asynccontextmanager

import json

from pathlib import Path

from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api_v1.users.views import router as users_router
from src.api_v1.auth.views import router as auth_router
from src.api_v1.universal_for_test.views import (router
                                                 as universal_tests_router)
from src.api_v1.tests.views import router as random_tests_router
from src.api_v1.topics.views import router as topics_router
from src.api_v1.story.views import router as story_router
from src.api_v1.static_test.views import router as static_tests_router
from src.api_v1.rewards.views import router as rewards_router
from src.api_v1.cases.views import router as cases_router
from src.api_v1.leaderboard.views import router as leaderboard_router
from src.core.config import settings
from src.core.models import db_helper
from src.core.redis import redis_client

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
IMAGES_DIR = STATIC_DIR / "images"
TOPICS_IMG_DIR = IMAGES_DIR / "sections_topics"
STORY_IMG_DIR = IMAGES_DIR / "story"

for folder in [TOPICS_IMG_DIR, STORY_IMG_DIR]:
    folder.mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(RedisBackend(redis_client), prefix='fastapi-cache')
    yield
    await redis_client.close()
    await db_helper.dispose()

app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.include_router(users_router, prefix=settings.api.prefix)
app.include_router(auth_router, prefix=settings.api.prefix)
app.include_router(universal_tests_router, prefix=settings.api.prefix)
app.include_router(random_tests_router, prefix=settings.api.prefix)
app.include_router(static_tests_router, prefix=settings.api.prefix)
app.include_router(topics_router, prefix=settings.api.prefix)
app.include_router(story_router, prefix=settings.api.prefix)
app.include_router(rewards_router, prefix=settings.api.prefix)
app.include_router(cases_router, prefix=settings.api.prefix)
app.include_router(leaderboard_router, prefix=settings.api.prefix)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

openapi_schema = app.openapi()
with open("openapi.json", "w") as f:
    json.dump(openapi_schema, f)

if __name__ == '__main__':
    uvicorn.run(
        'src.main:app',
        host=settings.run.host,
        port=settings.run.port
    )
