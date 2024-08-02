from fastapi import FastAPI, Request, Response
import logging
# from fastapi.middleware.cors import CORSMiddleware


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.get("/")
def home():
    return {"Hello" : "Weorld"}

@app.get("/sayname/{name}")
def say(name: str):
    return {"Hello" : name}
