import json
from pathlib import Path

from rank_bm25 import BM25Okapi


ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data" / "hr_faq.jsonl"


def load_docs(path: Path):
    docs = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            text = f"{row['question']} {row['answer']}"
            docs.append((row["id"], text))
    return docs


def main():
    docs = load_docs(DATA_FILE)
    corpus = [text.lower().split() for _, text in docs]
    bm25 = BM25Okapi(corpus)

    query = "How do I request remote work approval?"
    scores = bm25.get_scores(query.lower().split())
    top = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)[:5]

    print("\nSeason 0 / Ep 00 - BM25")
    print(f"Query: {query}\n")
    for (doc_id, text), score in top:
        print(f"score={score:.2f} | doc={doc_id} | {text[:120]}...")


if __name__ == "__main__":
    main()
