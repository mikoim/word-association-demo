import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from hypercorn.asyncio import serve
from hypercorn.config import Config as HypercornConfig

import duckduckgo
from models import DistanceResponse, ImageResponse, PredictResponse, Word
from server_nlp import NLPManager

app = FastAPI()

# ドメインを跨ぐリクエストを受け付ける
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静的ファイル配信
app.mount("/www", StaticFiles(directory="www"), name="www")


# UIへリダイレクト
@app.get("/")
def home():
    return RedirectResponse(url="/www/index.html")


# 関連単語を取得
@app.get("/words", response_model=PredictResponse)
def predict_words(q: str):
    manager = NLPManager()
    manager.connect()
    results = manager.predict(q)  # Proxy
    results = results.get("results")

    return PredictResponse(
        words=[Word(word=x[1], cosine_similarity=x[0]) for x in results]
    )


# 単語から画像を検索
@app.get("/images", response_model=ImageResponse)
def search_image(q: str):
    return ImageResponse(word=q, urls=[y["image"] for y in duckduckgo.search(q)])


# 単語間のコサイン類似度を取得
@app.get("/distance", response_model=DistanceResponse)
def predict_words(word_a: str, word_b):
    manager = NLPManager()
    manager.connect()
    result = manager.distance(word_a, word_b)  # Proxy
    return DistanceResponse(
        word_a=word_a, word_b=word_b, cosine_similarity=result.get("result")
    )


if __name__ == "__main__":
    hypercorn_config = HypercornConfig()
    hypercorn_config.bind = ["0.0.0.0:8888"]
    asyncio.run(serve(app, config=hypercorn_config))
