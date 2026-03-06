import json
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer


ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data" / "hr_faq.jsonl"


def load_docs(path: Path):
    docs = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            docs.append((row["id"], f"{row['question']} {row['answer']}"))
    return docs


def mean_pool(last_hidden_state: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
    mask = attention_mask.unsqueeze(-1).expand(last_hidden_state.size()).float()
    summed = (last_hidden_state * mask).sum(dim=1)
    count = mask.sum(dim=1).clamp(min=1e-9)
    return summed / count


def embed_texts(model_name: str, texts: list[str], batch_size: int = 16) -> np.ndarray:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    model.eval()

    all_vecs = []
    with torch.no_grad():
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            enc = tokenizer(batch, padding=True, truncation=True, return_tensors="pt", max_length=256)
            out = model(**enc)
            pooled = mean_pool(out.last_hidden_state, enc["attention_mask"])
            all_vecs.append(pooled.cpu().numpy())
    return np.vstack(all_vecs)


def cosine_scores(query_vec: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    q = query_vec / (np.linalg.norm(query_vec) + 1e-12)
    m = matrix / (np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-12)
    return m @ q


def main():
    docs = load_docs(DATA_FILE)
    doc_texts = [text for _, text in docs]

    model_name = "bert-base-uncased"
    doc_vecs = embed_texts(model_name, doc_texts)

    query = "How do I get travel expense reimbursement approved?"
    query_vec = embed_texts(model_name, [query])[0]
    scores = cosine_scores(query_vec, doc_vecs)

    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)[:5]

    print("\nSeason 0 / Ep 05 - BERT Embedding Retrieval")
    print(f"Embedding model: {model_name}")
    print(f"Query: {query}\n")
    for (doc_id, text), score in ranked:
        print(f"sim={score:.4f} | doc={doc_id} | {text[:120]}...")


if __name__ == "__main__":
    main()
