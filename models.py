from pydantic import BaseModel


class Word(BaseModel):
    word: str
    cosine_similarity: float


class PredictResponse(BaseModel):
    words: list[Word]


class DistanceResponse(BaseModel):
    word_a: str
    word_b: str
    cosine_similarity: float


class ImageResponse(BaseModel):
    word: str
    urls: list[str]
