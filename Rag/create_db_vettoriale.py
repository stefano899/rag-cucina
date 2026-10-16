from config import LLM_EMBEDDING_MODEL, PDF_DIR, DB_DIR
from chunk_separator import convert_pdf_in_chunks
import llm_client
import chromadb
import glob
import os
# Da lanciare una volta sola

# il cassetto si apre una volta sola, poi ci mettiamo dentro i libri uno alla volta
chroma_client = chromadb.PersistentClient(path = DB_DIR)

collection = chroma_client.get_or_create_collection(name="ricette")

for pdf in glob.glob(f"{PDF_DIR}/*.pdf"):

    chunk_list, text_list = convert_pdf_in_chunks(pdf)

    if len(text_list) == 0:
        print(f"Nessuna ricetta trovata in {pdf}")
        continue

    # crea una lista di id: il nome del file evita che i libri si sovrascrivano a vicenda
    list_id = []
    for i in range(len(text_list)):
        list_id.append(f"{os.path.basename(pdf)}_{i}")



    # calcolare gli embeddings
    embeddings = llm_client.client.embeddings.create(model=LLM_EMBEDDING_MODEL, input=text_list)
    list_embeddings = []

    for elem in embeddings.data:
        list_embeddings.append(elem.embedding)

    collection.upsert(ids=list_id, embeddings= list_embeddings, documents=text_list, metadatas=chunk_list)

    print(f"{os.path.basename(pdf)}: {len(text_list)} ricette")

print(collection.count())
