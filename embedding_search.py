# -*- coding: utf-8 -*-
# 약품 DB 의미 기반 벡터 검색 (문장 임베딩 + FAISS)
# 제품명 LIKE 매칭이 못 잡는 오타/증상 질의를 코사인 유사도 top-k로 검색한다.
import os
import pickle
import numpy as np
import pandas as pd
import drug_category

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_CSV = os.path.join(BASE_DIR, "data2.csv")
INDEX_DIR = os.path.join(BASE_DIR, "vector_index")
INDEX_PATH = os.path.join(INDEX_DIR, "drug.faiss")
META_PATH = os.path.join(INDEX_DIR, "drug_meta.pkl")

MODEL_NAME = os.environ.get("EMBED_MODEL", "intfloat/multilingual-e5-base")
QUERY_PREFIX = "query: "
PASSAGE_PREFIX = "passage: "

TEXT_COLUMNS = ["제품명", "업체명", "ATC코드 명칭", "약효분류"]
META_COLUMNS = ["제품명", "업체명", "ATC코드 명칭", "식약분류", "약효분류", "ATC코드"]


def row_to_text(row):
    parts = [str(row.get(c, "")).strip() for c in TEXT_COLUMNS]
    return " / ".join(p for p in parts if p)


class DrugVectorSearch:
    def __init__(self, model_name=MODEL_NAME):
        self.model_name = model_name
        self._model = None
        self.index = None
        self.meta = None

    @property
    def model(self):
        if self._model is None:  # 무거운 임베딩 모델은 최초 사용 시 1회만 로드
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def _encode(self, texts, prefix):
        emb = self.model.encode(
            [prefix + t for t in texts],
            batch_size=64,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False
        )
        return emb.astype("float32")

    def build(self, csv_path=DATA_CSV, save=True):
        import faiss
        df = pd.read_csv(csv_path, dtype=str).fillna("")
        df["약효분류"] = df["식약분류"].map(drug_category.name_of)
        df = df.drop_duplicates(subset=["제품명", "ATC코드 명칭"]).reset_index(drop=True)

        emb = self._encode([row_to_text(r) for _, r in df.iterrows()], PASSAGE_PREFIX)
        self.index = faiss.IndexFlatIP(emb.shape[1])
        self.index.add(emb)
        self.meta = df[META_COLUMNS].to_dict("records")

        if save:
            os.makedirs(INDEX_DIR, exist_ok=True)
            # 한글 경로에서 faiss.write_index가 실패하므로 바이트로 직렬화해 저장한다.
            with open(INDEX_PATH, "wb") as f:
                f.write(faiss.serialize_index(self.index).tobytes())
            with open(META_PATH, "wb") as f:
                pickle.dump({"model_name": self.model_name, "meta": self.meta}, f)
        return self

    def load(self):
        import faiss
        with open(INDEX_PATH, "rb") as f:
            self.index = faiss.deserialize_index(np.frombuffer(f.read(), dtype="uint8"))
        with open(META_PATH, "rb") as f:
            payload = pickle.load(f)
        self.model_name = payload["model_name"]
        self.meta = payload["meta"]
        return self

    def ensure_ready(self):
        if self.index is not None and self.meta is not None:
            return self
        if os.path.exists(INDEX_PATH) and os.path.exists(META_PATH):
            return self.load()
        return self.build()

    def search(self, query, top_k=5):
        self.ensure_ready()
        scores, idxs = self.index.search(self._encode([query], QUERY_PREFIX), top_k)
        results = []
        for score, i in zip(scores[0], idxs[0]):
            if i < 0:
                continue
            item = dict(self.meta[i])
            item["score"] = float(score)
            results.append(item)
        return results

    def format_for_prompt(self, query, top_k=5):
        results = self.search(query, top_k)
        if not results:
            return "[의미 기반 약품 검색 결과]\n없음"
        lines = [f"[의미 기반 약품 검색 결과 (벡터 유사도 top-{top_k})]"]
        for rank, r in enumerate(results, 1):
            lines.append(
                f"{rank}. 제품명: {r.get('제품명', '')} "
                f"| 성분/ATC명칭: {r.get('ATC코드 명칭', '')} "
                f"| 약효: {r.get('약효분류', '')} "
                f"| 유사도: {r['score']:.3f}"
            )
        return "\n".join(lines)


_searcher = None


def get_searcher():
    global _searcher
    if _searcher is None:
        _searcher = DrugVectorSearch().ensure_ready()
    return _searcher


if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "두통에 먹는 진통제"
    print(DrugVectorSearch().ensure_ready().format_for_prompt(query))
