import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data" / "hr_faq.jsonl"


def load_docs(path: Path):
    docs = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            docs.append((row["id"], f"{row['question']} {row['answer']}"))
    return docs


def cosine_scores(query_vec: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    q = query_vec / (np.linalg.norm(query_vec) + 1e-12)
    m = matrix / (np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-12)
    return m @ q


def run_for_model(model_name: str, query: str, docs: list[tuple[int, str]], top_k: int = 3):
    model = SentenceTransformer(model_name)
    doc_texts = [t for _, t in docs]
    doc_vecs = model.encode(doc_texts, normalize_embeddings=True)
    q_vec = model.encode([query], normalize_embeddings=True)[0]
    scores = cosine_scores(q_vec, doc_vecs)
    return sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)[:top_k]


def main():
    docs = load_docs(DATA_FILE)
    query = "What is the process for parental leave approval?"
    models = [
        "all-MiniLM-L6-v2",
        "intfloat/e5-small-v2",
    ]

    print("\nSeason 0 / Ep 06 - Embedding Model Comparison")
    print(f"Query: {query}\n")
    for model_name in models:
        print(f"Model: {model_name}")
        top = run_for_model(model_name, query, docs)
        for (doc_id, text), score in top:
            print(f"  sim={score:.4f} | doc={doc_id} | {text[:90]}...")
        print()


if __name__ == "__main__":
    main()
