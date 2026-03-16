import sqlite3
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "data" / "company_store.db"


def fetch_short_term_history():
    return [
        "User asked about recent order count",
        "User then asked for top spending customer",
    ]


def tokenize(text: str) -> list[str]:
    return [w.strip(".,!?;:()[]{}\"'").lower() for w in text.split() if w.strip()]


def tfidf_matrix(texts: list[str]) -> np.ndarray:
    tokenized = [tokenize(t) for t in texts]
    vocab = sorted({tok for doc in tokenized for tok in doc})
    index = {w: i for i, w in enumerate(vocab)}

    tf = np.zeros((len(texts), len(vocab)), dtype=np.float64)
    for row, doc in enumerate(tokenized):
        if not doc:
            continue
        for tok in doc:
            tf[row, index[tok]] += 1.0
        tf[row] /= len(doc)

    df = np.zeros(len(vocab), dtype=np.float64)
    for j, word in enumerate(vocab):
        df[j] = sum(1 for doc in tokenized if word in set(doc))

    n_docs = len(texts)
    idf = np.log((1 + n_docs) / (1 + df)) + 1.0
    return tf * idf


def cosine_scores(query_vec: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    q = query_vec / (np.linalg.norm(query_vec) + 1e-12)
    m = matrix / (np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-12)
    return m @ q


def fetch_long_term_memory(query: str, k: int = 2):
    memories = [
        "Orders table links user_id and product_id",
        "High-value products are typically in Laptop category",
        "Users table contains city metadata",
        "Orders include quantity and timestamp",
    ]
    matrix = tfidf_matrix(memories + [query])
    sims = cosine_scores(matrix[-1], matrix[:-1])
    ranked = sorted(zip(memories, sims), key=lambda x: x[1], reverse=True)
    return [m for m, _ in ranked[:k]]


def sql_observation() -> str:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Orders")
    count = cur.fetchone()[0]
    conn.close()
    return f"Orders count = {count}"


def main():
    query = "How can I analyze highest spenders by city?"
    short_mem = fetch_short_term_history()
    long_mem = fetch_long_term_memory(query)
    obs = sql_observation()

    print("\nSeason 1 / Ep 03 - Level 3 Memory Injection")
    print("Short-term memory:")
    for item in short_mem:
        print("-", item)
    print("\nLong-term memory:")
    for item in long_mem:
        print("-", item)
    print("\nTool observation:", obs)


if __name__ == "__main__":
    main()
