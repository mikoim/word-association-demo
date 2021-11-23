from pydantic import BaseModel


class Word(BaseModel):
    name: str
    cosine_similarity: float
    images: list[str]


class PredictResponse(BaseModel):
    words: list[Word]
