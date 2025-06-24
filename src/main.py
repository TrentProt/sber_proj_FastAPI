from contextlib import asynccontextmanager

import json

from pathlib import Path

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api_v1.users.views import router as users_router
from src.api_v1.auth.views import router as auth_router
from src.api_v1.universal_for_test.views import router as universal_tests_router
from src.api_v1.tests.views import router as random_tests_router
from src.api_v1.topics.views import router as topics_router
from src.api_v1.story.views import router as story_router
from src.api_v1.static_test.views import router as static_tests_router
from src.api_v1.rewards.views import router as rewards_router
from src.api_v1.cases.views import router as cases_router
from src.core.redis import redis_client

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
IMAGES_DIR = STATIC_DIR / "images"
TOPICS_IMG_DIR = IMAGES_DIR / "sections_topics"
STORY_IMG_DIR = IMAGES_DIR / "story"

for folder in [TOPICS_IMG_DIR, STORY_IMG_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # async with db_helper.engine.begin() as conn:
#     #     await conn.run_sync(Base.metadata.create_all)
#     yield

@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(RedisBackend(redis_client), prefix='fastapi-cache')
    yield
    await redis_client.close()

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(universal_tests_router)
app.include_router(random_tests_router)
app.include_router(static_tests_router)
app.include_router(topics_router)
app.include_router(story_router)
app.include_router(rewards_router)
app.include_router(cases_router)


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
    uvicorn.run('src.main:app')