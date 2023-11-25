import os
from tqdm import tqdm
import chromadb
from langchain.embeddings import GPT4AllEmbeddings

class ChromaInserter:
    def __init__(self):
        self.gpt4all_embd = GPT4AllEmbeddings()
        self.client_chroma = chromadb.PersistentClient(path=os.getenv("CHROMA_DB_PATH"))
        self.collection = self.client_chroma.get_or_create_collection(os.getenv("CHROMA_COLLECTION_NAME"))


    def insert_final_data(self, final_data):
        idX = 0

        for data in tqdm(final_data):
            doc_result = self.gpt4all_embd.embed_query(data)

            self.collection.add(
                embeddings=[doc_result],
                documents=[data],
                metadatas=[{"source": "batch"}],
                ids=[str(idX)]
            )
            idX += 1