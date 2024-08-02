from fastapi import FastAPI, Request, Response
import logging
from fastapi.middleware.cors import CORSMiddleware
from api.home_api import router as home_router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(home_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from localhost on port 80
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)



@app.get("/api/hello")
def home():
    return {"Hello" : "Weorld"}

@app.get("/api/sayname/{name}")
def say(name: str):
    return {"Hello" : name}
