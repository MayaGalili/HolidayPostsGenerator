import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

def run_ingestion():

    load_dotenv(override=True)

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small"
    )
    client = chromadb.PersistentClient(path="./chroma_db_data")
    collection = client.get_or_create_collection(
        name="company_knowledge_base", 
        embedding_function=openai_ef
    )

    docs_dir = "./resources/company_documents"
    documents = []
    ids = []

    for idx, filename in enumerate(os.listdir(docs_dir)):
        if filename.endswith(".txt"):
            with open(os.path.join(docs_dir, filename), "r", encoding="utf-8") as f:
                documents.append(f.read())
                ids.append(f"doc_{idx}")

    collection.add(documents=documents, ids=ids)
    print("Data ingestion complete!")

if __name__ == "__main__":
    run_ingestion()