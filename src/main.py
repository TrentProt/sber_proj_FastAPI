from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI

from src.core.models.users import Users
from src.users.views import router as users_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    # async with db_helper.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users_router)



if __name__ == '__main__':
    uvicorn.run('src.main:app')