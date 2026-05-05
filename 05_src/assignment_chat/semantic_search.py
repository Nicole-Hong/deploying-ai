
import os
from pathlib import Path

import chromadb
from openai import OpenAI

client = OpenAI()

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "transit_ai_knowledge.md"
CHROMA_DIR = BASE_DIR / "chroma_db"

COLLECTION_NAME = "transit_ai_knowledge"


def chunk_text(text: str, chunk_size: int = 500):
    """
    Simple chunking strategy.
    Keeps the project small and easy to explain.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []

    current = ""

    for paragraph in paragraphs:
        if len(current) + len(paragraph) <= chunk_size:
            current += "\n\n" + paragraph
        else:
            if current.strip():
                chunks.append(current.strip())
            current = paragraph

    if current.strip():
        chunks.append(current.strip())

    return chunks


def embed_texts(texts):
    """
    Creates OpenAI embeddings.
    """
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )

    return [item.embedding for item in response.data]


def get_collection():
    """
    Creates or loads a persistent ChromaDB collection.
    """
    chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


def build_vector_store_if_needed():
    """
    Builds the ChromaDB vector store only if it is empty.
    """
    collection = get_collection()

    if collection.count() > 0:
        return collection

    text = DATA_FILE.read_text(encoding="utf-8")
    chunks = chunk_text(text)

    embeddings = embed_texts(chunks)

    ids = [f"doc_{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=[{"source": "transit_ai_knowledge.md"} for _ in chunks]
    )

    return collection


def semantic_query(user_question: str) -> str:
    """
    Service 2: Semantic search service.
    """
    collection = build_vector_store_if_needed()

    query_embedding = embed_texts([user_question])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )

    documents = results.get("documents", [[]])[0]

    if not documents:
        return "I could not find relevant information in the knowledge base."

    context = "\n\n".join(documents)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer the user's question using only the provided knowledge base context. "
                    "If the context is limited, say so clearly."
                )
            },
            {
                "role": "user",
                "content": f"""
User question:
{user_question}

Knowledge base context:
{context}
"""
            }
        ]
    )

    return response.choices[0].message.content