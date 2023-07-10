from typing import Union
from fastapi import FastAPI
from fastapi.responses import JSONResponse


app = FastAPI()


@app.get("/")
async def health_check():
    response = {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }
    return JSONResponse(content=response)


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}