from fastapi import FastAPI

from .controllers.auth_controller import auth_router
from .controllers.my_balance_controller import my_balance_router

app = FastAPI()

app.include_router(router=auth_router)
app.include_router(router=my_balance_router)
