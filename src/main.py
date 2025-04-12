from fastapi import FastAPI

import uvicorn

from src.users.views import router as users_router

app = FastAPI()
app.include_router(users_router)

if __name__ == '__main__':
    uvicorn.run('src.main:app')