from orders.api.api import router
from fastapi import FastAPI

app = FastAPI(debug=True)
app.include_router(router)
