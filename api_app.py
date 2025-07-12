from fastapi import FastAPI
import os
from pathlib import Path
from api import endpoints
from fastapi.middleware.cors import CORSMiddleware
import logging
from logging.config import fileConfig 

os.chdir(Path(__file__).parent)

app = FastAPI(title="Sentiment Analysis API")
fileConfig("./logging.ini")
logger = logging.getLogger("backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:3000"], # api and app running on same machine atm, so no effect
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router)
logger.info("API initialized and router included.")