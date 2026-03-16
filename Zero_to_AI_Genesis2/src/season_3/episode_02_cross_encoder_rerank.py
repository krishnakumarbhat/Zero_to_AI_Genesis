import json
from pathlib import Path

import numpy as np
from sentence_transformers import CrossEncoder, SentenceTransformer


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
    docs = load_docs(DATA_FILE)
    query = "How quickly does HR approve PTO requests?"

    bi_encoder = SentenceTransformer("all-MiniLM-L6-v2")
    doc_texts = [text for _, text in docs]
    doc_vecs = bi_encoder.encode(doc_texts, normalize_embeddings=True)
    query_vec = bi_encoder.encode([query], normalize_embeddings=True)[0]
    dense_scores = cosine_scores(query_vec, doc_vecs)

    top50 = sorted(zip(docs, dense_scores), key=lambda x: x[1], reverse=True)[:50]
    candidate_texts = [text for (_, text), _ in top50]

    cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    pairs = [[query, text] for text in candidate_texts]
    rerank_scores = cross_encoder.predict(pairs)

    final_rank = sorted(
        zip(top50, rerank_scores),
        key=lambda x: x[1],
        reverse=True,
    )[:5]

    print("\nSeason 0 / Ep 02 - Cross-Encoder Re-ranking")
    print(f"Query: {query}\n")
    for ((doc, _dense_score), cross_score) in final_rank:
        doc_id, text = doc
        print(f"cross={cross_score:.4f} | doc={doc_id} | {text[:120]}...")


if __name__ == "__main__":
    main()
