from pinecone import Pinecone

import os
from dotenv import load_dotenv

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("mini-serach")

def store_embeddings(chunks, embeddings, pdf_name):
    vectors = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        vectors.append({
            "id": pdf_name+" "+str(i),          
            "values":  embedding.tolist(),  
            "metadata": {
                "text": chunk,    
                "source": pdf_name   
            }
        })
    index.upsert(vectors=vectors)

def search(query_embedding, top_k=3):
    results = index.query(
        vector=query_embedding ,
        top_k= top_k ,
        include_metadata=True
    )
    return results