import json
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, StateGraph
from llama_index.core import Document, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data" / "hr_faq.jsonl"


class RAGState(TypedDict):
    query: str
    context: str
    answer: str


def load_documents(path: Path):
    docs = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            text = f"Q: {row['question']}\nA: {row['answer']}\nTopic: {row['topic']}"
            docs.append(Document(text=text, metadata={"id": row["id"], "topic": row["topic"]}))
    return docs


def build_retriever():
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    index = VectorStoreIndex.from_documents(load_documents(DATA_FILE), embed_model=embed_model)
    return index.as_retriever(similarity_top_k=4)


def retrieve_node(state: RAGState) -> RAGState:
    retriever = build_retriever()
    nodes = retriever.retrieve(state["query"])
    context = "\n\n".join([n.get_content() for n in nodes])
    return {**state, "context": context}


def generate_node(state: RAGState) -> RAGState:
    answer = (
        "RAG answer (extractive summary):\n"
        f"Question: {state['query']}\n"
        "Relevant policy snippets:\n"
        f"{state['context'][:900]}"
    )
    return {**state, "answer": answer}


def build_graph():
    graph = StateGraph(RAGState)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("generate", generate_node)
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)
    return graph.compile()


def main():
    app = build_graph()
    query = "What is the process for expense reimbursement and approval timing?"
    result = app.invoke({"query": query, "context": "", "answer": ""})

    print("\nSeason 0 / Ep 09 - LlamaIndex + LangGraph RAG")
    print(result["answer"])


if __name__ == "__main__":
    main()
