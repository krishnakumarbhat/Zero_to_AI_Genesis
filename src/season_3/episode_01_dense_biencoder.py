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


def main():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    docs = load_docs(DATA_FILE)
    doc_texts = [text for _, text in docs]
    doc_vecs = model.encode(doc_texts, normalize_embeddings=True)

    query = "What is the reimbursement flow for travel expenses?"
    query_vec = model.encode([query], normalize_embeddings=True)[0]
    sim = cosine_scores(query_vec, doc_vecs)

    ranked = sorted(zip(docs, sim), key=lambda x: x[1], reverse=True)[:5]
    print("\nSeason 0 / Ep 01 - Dense Retrieval")
    print(f"Query: {query}\n")
    for (doc_id, text), score in ranked:
        print(f"sim={score:.4f} | doc={doc_id} | {text[:120]}...")


if __name__ == "__main__":
    main()
