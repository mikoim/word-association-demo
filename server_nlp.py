from multiprocessing.managers import SyncManager

import fasttext.util
import numpy as np

FT = None


def predict(word: str) -> dict:
    """
    モデル上において入力単語の近傍に位置する単語を取得する

    :param word: 入力単語
    :return: 入力単語の近傍に位置する単語のリスト
    """
    return {
        "results": FT.get_nearest_neighbors(word, k=20)
    }  # SyncManagerの仕様上, プリミティブ型を返せないためラップ


def distance(word_a: str, word_b: str) -> dict:
    """
    モデル上における2単語のベクトル表現間のコサイン類似度を求める

    :param word_a: 単語A
    :param word_b: 単語B
    :return: コサイン類似度
    """
    x = FT.get_word_vector(word_a)
    y = FT.get_word_vector(word_b)

    return {
        "result": np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))
    }  # SyncManagerの仕様上, プリミティブ型を返せないためラップ


class NLPManager(SyncManager):
    def __init__(self):
        self.register("predict", predict)
        self.register("distance", distance)
        super().__init__(("0.0.0.0", 9999), authkey=b"nlp")


def main():
    global FT

    print("モデルを読み込み中...")
    fasttext.util.download_model("ja", if_exists="ignore")
    FT = fasttext.load_model("cc.ja.300.bin")
    FT.get_nearest_neighbors("家族")  # ウォームアップ
    print("完了")

    manager = NLPManager()
    manager.get_server().serve_forever()


if __name__ == "__main__":
    main()
