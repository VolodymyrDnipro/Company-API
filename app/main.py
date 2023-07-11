from typing import Union
from fastapi import FastAPI

from uvicorn import Config, Server

from config import settings

app = FastAPI()


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
    server = Server(
        Config(
            app,
            host=settings.SERVER_HOST,
            port=settings.SERVER_PORT,
        ),
    )
    server.run()
