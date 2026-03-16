import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data" / "wiki_like_articles.jsonl"


def chunk_text(text: str, chunk_size: int = 12):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i : i + chunk_size])


def cosine_scores(query_vec: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    q = query_vec / (np.linalg.norm(query_vec) + 1e-12)
    m = matrix / (np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-12)
    return m @ q


def main():
    docs = []
    with DATA_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            docs.append(row)

    child_chunks = []
    child_to_parent = {}
    for row in docs:
        parent_id = row["id"]
        for idx, chunk in enumerate(chunk_text(row["text"], chunk_size=10)):
            child_id = f"{parent_id}-c{idx}"
            child_chunks.append((child_id, chunk))
            child_to_parent[child_id] = parent_id

    model = SentenceTransformer("all-MiniLM-L6-v2")
    child_texts = [c for _, c in child_chunks]
    child_vecs = model.encode(child_texts, normalize_embeddings=True)

    query = "How did printing improve scientific communication?"
    q_vec = model.encode([query], normalize_embeddings=True)[0]
    scores = cosine_scores(q_vec, child_vecs)
    ranked_children = sorted(zip(child_chunks, scores), key=lambda x: x[1], reverse=True)[:5]

    parent_scores = defaultdict(float)
    for ((child_id, _chunk), score) in ranked_children:
        parent_scores[child_to_parent[child_id]] += float(score)

    ranked_parents = sorted(parent_scores.items(), key=lambda x: x[1], reverse=True)
    parent_lookup = {d["id"]: d for d in docs}

    print("\nSeason 0 / Ep 03 - Parent-Child Chunking")
    print(f"Query: {query}\n")
    for parent_id, score in ranked_parents:
        print(f"parent={parent_id} score={score:.4f} title={parent_lookup[parent_id]['title']}")
        print(parent_lookup[parent_id]["text"])
        print()


if __name__ == "__main__":
    main()
