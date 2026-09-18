# 환경·건강 LLM RAG 챗봇 (AI 처방카드)

사용자의 환경·건강 데이터를 프롬프트에 주입하고, 약품 질의는 검색 근거로 답하는 **RAG 챗봇**이다.
연구 용역에서 개발했으며, 저장소에는 RAG 파이프라인 코어만 담았다. (데이터 수집기·DB 설정·데이터 파일은 제외)

<br>

## 파이프라인

```
질의 입력
 └─ 라우팅(LLM 분류): 약품 / 일반
      ├─ 약품 → 하이브리드 검색(임베딩 의미검색 + Text-to-SQL) → LLM 응답
      └─ 일반 → 환경·건강 데이터 프롬프트 주입 → LLM 스트리밍 응답
```

<br>

## 구성

- **임베딩 의미 검색** (`embedding_search.py`, `build_index.py`)
  - 의약품 DB를 문장 임베딩(multilingual-e5)으로 인덱싱, **FAISS 코사인 유사도 top-k** 검색
  - 증상·오타 질의도 의미 기반으로 매칭
- **약효 분류 매핑** (`drug_category.py`)
  - ATC/약효분류 코드 → 한글 약효명으로 검색 텍스트 보강
- **Text-to-SQL** (`prompt/system_B.txt`)
  - 제품명 정확 매칭은 SQL 에이전트로 병행 (하이브리드)
- **프롬프트 구성** (`make_prompt.py`, `prompt/system.txt`)
  - 환경·건강 컨텍스트 주입, 시스템 규칙 정의
- **LLM 서빙** (`pred_llm.py`)
  - 로컬 LLM(Ollama, LLaMA3 계열)을 OpenAI 호환 스트리밍 API로 호출

<br>

## 메모

- 환경·건강 데이터를 수집하는 모듈(외부 API·DB 연동)과 의약품 데이터(CSV)는 포함하지 않는다.
- 서버 주소·자격증명은 환경변수로 주입한다.

<br>

## 기술 스택

Python · LangChain · FAISS · sentence-transformers(multilingual-e5) · Ollama(LLaMA3) · Text-to-SQL · Docker
