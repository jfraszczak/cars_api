from fastapi import FastAPI, Response
from . import cars

app = FastAPI()
app.include_router(cars.router)

@app.get("/")
async def root():
    return Response('Server is running')