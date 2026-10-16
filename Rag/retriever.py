import config
import llm_client
import chromadb


def retrieve_question(question, n_results = 10):
    # calcola l'embedding della domanda
    embedding = llm_client.client.embeddings.create(model=config.LLM_EMBEDDING_MODEL, input=question)
    embedding_question = embedding.data[0].embedding
    
    # richiamiamo il db: collegamento e andiamo verso le ricette
    chroma_client = chromadb.PersistentClient(path=config.DB_DIR)
    collection = chroma_client.get_collection(name="ricette")

    # Cerchiamo le ricette più vicine al vettore della domanda
    # L'algoritmo che utilizza è il K-Nearest Neighbor
    results = collection.query(query_embeddings=[embedding_question], n_results=n_results)

    return results



if __name__ == "__main__":
    question = "Mi dici la ricetta che consiglia un vino rosso?"
    results = retrieve_question(question)

    for i, r in enumerate(results["metadatas"][0], start=1):
        print(f"{i}. {r['title'].capitalize()} (pag. {r['page_number']})")
