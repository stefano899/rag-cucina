from config import PDF_DIR
import pymupdf4llm
import re

def is_ricetta(text):
    rows = text.split("\n")
    for row in rows:
        rows_clean = pulisci_riga(row).replace(" ", "")
        if rows_clean.startswith("ingredienti"):
            return True

    return False

def pulisci_riga(row):
    row_clean = re.sub(r"<[^>]+>", "", row).strip("#*_ ")
    return row_clean

def convert_pdf_in_chunks(path):

    pagine = pymupdf4llm.to_markdown(path, page_chunks = True)
    chunk_list = []
    text_list = []
    for i in range(len(pagine)):
        if is_ricetta(pagine[i]['text'].lower()):
            chunk = {}
            text = pagine[i]['text']

            # se la pagina inizia direttamente con "Ingredienti" il titolo è nella pagina prima
            prima_riga_pagina = text.strip().split("\n")[0]
            if i > 0 and is_ricetta(prima_riga_pagina.lower()):
                pagina_prima = pagine[i-1]['text'].strip()
                if len(pagina_prima) >= 1 and len(pagina_prima) <= 99:
                    text = pagina_prima + "\n\n" + text

            # attacca le pagine dopo finché sono lunghe e non iniziano una nuova ricetta
            j = i + 1
            while j < len(pagine) and len(pagine[j]['text'].strip()) >= 100 and not is_ricetta(pagine[j]['text'].lower()):
                text = text + "\n\n" + pagine[j]['text']
                j = j + 1

            metadata = pagine[i]['metadata']
            prima_riga = text.strip().split("\n")[0]
            title_no_spaces = pulisci_riga(prima_riga)
            print(title_no_spaces)
            chunk['title'] = title_no_spaces
            chunk['page_number'] = metadata['page_number']
            chunk['file_path'] = metadata['file_path']
            chunk_list.append(chunk)
            text_list.append(text)
    return chunk_list, text_list


if __name__ == "__main__":
    path = f"{PDF_DIR}/Ricettario_ITA.pdf"
    chunk_list, text_list = convert_pdf_in_chunks(path)

    print(len(text_list))
    #print(text_list[0])
