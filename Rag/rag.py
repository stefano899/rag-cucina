import config
import llm_client
import retriever

def write_question():
    question = input("Scrivi la domanda qui, ci penserò io a restituire la risposta: ")

    rag_answer = retriever.retrieve_question(question)
    ricette = "\n\n".join(rag_answer["documents"][0])
    question_and_rag = f"Ricette:\n{ricette}\n\nDomanda: {question}"

    response = llm_client.client.chat.completions.create(
    model=config.MODEL,
    messages=[
        {"role": "system", "content": "Sei un assistente di cucina, di conseguenza risponderai"
        " solo a domande che riguardano la cucina e in particolar modo alle ricette. Quando risponderai dovrai "
        " restituire le fonti degli elementi da cui hai effettuato la risposta e dare la motivazione del perchè hai scelto queste"
        " ricette da consigliarmi. Usa solo le ricette fornite assieme alla domanda. Utilizza un linguaggio naturale quando descrivi "
        "le ricette e fai dei bullet points per separare le fasi delle ricette"},
        {"role": "user", "content": question_and_rag}
    ]
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    write_question()
