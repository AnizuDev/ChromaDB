import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

def init_chroma(collection_name: str):
    client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="./chroma_store"
    ))

    return client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_functions.DefaultEmbeddingFunction()
    )

def add_documents(collection, anime_list):
    for anime in anime_list:
        title = anime.get("title", {}).get("romaji", "Unknown")
        description = anime.get("summary", "")
        genres = ", ".join(anime.get("genres", []))
        year = anime.get("firstAirDate", "Unknown")

        content = f"""
        Title: {title}
        Description: {description}
        Genres: {genres}
        Year: {year}
        """.strip()

        collection.add(
            documents=[content],
            ids=[anime.get("_id")],
            metadatas=[anime]
        )

def search_documents(collection, query, k=5):
    result = collection.query(query_texts=[query], n_results=k)
    return [
        {
            "id": result["ids"][0][i],
            "score": result["distances"][0][i],
            "metadata": result["metadatas"][0][i]
        }
        for i in range(len(result["ids"][0]))
    ]

