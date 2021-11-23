# word-association-demo
Japanese word association demo implementation using [FastText](https://fasttext.cc/).

## Getting Started

```shell
pip install --user pipenv

git clone https://github.com/mikoim/word-association-demo.git
cd word-association-demo

pipenv install

pipenv run python server_api.py
pipenv run python server_nlp.py
```

## Specification

### API Server

#### GET /words?q=牡蠣

```json
{
  "related_words": {
    "牡蛎": [
      "https://example.com/hoge.jpg"
    ],
    "ホタテ": [
      "https://example.com/hoge.png"
    ],
    "海鮮": []
  }
}
```

### NLP Server

- predict(word: str) -> list[str]
