# -*- coding: utf-8 -*-
# 약품 임베딩 인덱스 사전 빌드. 최초 1회 실행하면 vector_index/ 에 저장된다.
from embedding_search import DrugVectorSearch

if __name__ == "__main__":
    s = DrugVectorSearch().build(save=True)
    print(f"인덱싱 완료: {len(s.meta)}건, 차원={s.index.d}")
