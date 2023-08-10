import uvicorn

from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from api.routers.users import users_router
from api.routers.auth import auth_router
from api.routers.company import company_router
from api.routers.quizzes import quiz_router
from api.routers.analytics import analytics_router
from api.routers.notifications import notifications_router

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


# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(auth_router, tags=["Auth"])
main_api_router.include_router(users_router, tags=["User"])
main_api_router.include_router(company_router, tags=["Company"])
main_api_router.include_router(quiz_router, tags=["Quizzes"])
main_api_router.include_router(analytics_router, tags=["Analytics"])
main_api_router.include_router(notifications_router, tags=["Notifications"])
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT, log_level="info")

