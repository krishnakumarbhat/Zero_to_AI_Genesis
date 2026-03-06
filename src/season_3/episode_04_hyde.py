import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data" / "wiki_like_articles.jsonl"


def load_docs(path: Path):
    docs = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            docs.append((row["id"], row["title"], row["text"]))
    return docs


def mock_hypothetical_answer(query: str) -> str:
    return (
        "Hypothetical answer: The printing press allowed low-cost replication of texts, "
        "which helped scholars share experiments, methods, and discoveries faster across regions. "
        f"Question was: {query}"
    )


def cosine_scores(query_vec: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    q = query_vec / (np.linalg.norm(query_vec) + 1e-12)
    m = matrix / (np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-12)
    return m @ q


def main():
    docs = load_docs(DATA_FILE)
    model = SentenceTransformer("all-MiniLM-L6-v2")

    doc_texts = [text for _, _, text in docs]
    doc_vecs = model.encode(doc_texts, normalize_embeddings=True)

    query = "Why did early science spread faster in Europe?"
    query_vec = model.encode([query], normalize_embeddings=True)[0]
    baseline_scores = cosine_scores(query_vec, doc_vecs)

    hyde_doc = mock_hypothetical_answer(query)
    hyde_vec = model.encode([hyde_doc], normalize_embeddings=True)[0]
    hyde_scores = cosine_scores(hyde_vec, doc_vecs)

    base_rank = sorted(zip(docs, baseline_scores), key=lambda x: x[1], reverse=True)[:3]
    hyde_rank = sorted(zip(docs, hyde_scores), key=lambda x: x[1], reverse=True)[:3]

    print("\nSeason 0 / Ep 04 - HyDE")
    print(f"Query: {query}\n")
    print("Baseline top-3:")
    for (doc_id, title, _), score in base_rank:
        print(f"{doc_id} | {title} | {score:.4f}")

    print("\nHyDE top-3:")
    for (doc_id, title, _), score in hyde_rank:
        print(f"{doc_id} | {title} | {score:.4f}")


if __name__ == "__main__":
    main()
