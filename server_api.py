import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from hypercorn.asyncio import serve
from hypercorn.config import Config as HypercornConfig

import duckduckgo
from models import PredictResponse, Word
from server_nlp import NLPManager

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/www", StaticFiles(directory="www"), name="www")


@app.get("/")
def home():
    return RedirectResponse(url="/www/index.html")


@app.get("/words", response_model=PredictResponse)
def predict_words(q: str):
    manager = NLPManager()
    manager.connect()
    results = manager.predict(q)  # Proxy
    return PredictResponse(
        words=[
            Word(name=x[1], cosine_similarity=x[0], images=[y["image"] for y in duckduckgo.search(x[1])])
            for x in results.get("results")
        ]
    )


if __name__ == "__main__":
    hypercorn_config = HypercornConfig()
    hypercorn_config.bind = ["0.0.0.0:8888"]
    asyncio.run(serve(app, config=hypercorn_config))
