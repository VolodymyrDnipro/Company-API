import uvicorn

from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from log import logger

# Запись логов
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")


app = FastAPI()

# Настройки CORS
origins = [
    settings.SERVER_HOST,
    settings.SERVER_PORT,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    response = {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }
    return response


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT, log_level="info")
