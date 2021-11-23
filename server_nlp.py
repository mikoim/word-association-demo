from multiprocessing.managers import SyncManager

import fasttext.util

FT = None


def predict(words: str) -> dict:
    return {"results": FT.get_nearest_neighbors(words, k=20)}  # Can't return raw values


class NLPManager(SyncManager):
    def __init__(self):
        self.register("predict", predict)
        super().__init__(("0.0.0.0", 9999), authkey=b"nlp")


def main():
    global FT

    print("Loading model...")
    fasttext.util.download_model("ja", if_exists="ignore")
    FT = fasttext.load_model("cc.ja.300.bin")
    FT.get_nearest_neighbors("家族")  # warm up
    print("done")

    manager = NLPManager()
    manager.get_server().serve_forever()


if __name__ == "__main__":
    main()
