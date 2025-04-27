from contextlib import asynccontextmanager
import json
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api_v1.users.views import router as users_router
from src.api_v1.auth.views import router as auth_router
from src.api_v1.tests.views import router as tests_router
from src.api_v1.topics.views import router as topics_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    # async with db_helper.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(tests_router)
app.include_router(topics_router)
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