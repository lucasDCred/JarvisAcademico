#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import os # Biblioteca para acessar arquivos

from rag.carregadorPDF import carregar_pdf # Retorna todo texto do PDF

from rag.chunker import dividir_chunks # Divide o texto dos PDFs em partes menores (chunks)

from rag.embeddings import (gerar_embeddings, modelo) # Gera vetores do texto

from rag.retriever import (criar_indice, buscar_chunks) # Índice vetorial e faz a busca dos chunks mais relevantes
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def buscar_material_rag(pergunta_usuario, comando_rag):

    arquivo_pdf = comando_rag.replace("USAR_RAG:", "").strip() # Separa USAR_RAG: e Nome_do_arquivo.pdf

    # Percorre a pasta documentos contendo os PDFs
    for arquivo in os.listdir("dados/documentos"):

        # Verifica se encontrou o PDF
        if arquivo == arquivo_pdf:

            print(f"Carregando: {arquivo}")

            caminho = f"dados/documentos/{arquivo}" # Caminho completo

            texto_pdf = carregar_pdf(caminho) # Carrega PDF

            chunks = dividir_chunks(texto_pdf) # Divide em chunks

            embeddings = gerar_embeddings(chunks) # Gera embeddings

            indice = criar_indice(embeddings) # Cria índice vetorial

            embedding_pergunta = modelo.encode(pergunta_usuario) # Gera embedding da pergunta do usuário

            chunks_encontrados = buscar_chunks(indice, embedding_pergunta, chunks) # Busca chunks relevantes
            
            contexto_rag = "\n".join(chunks_encontrados) # Junta chunks

            return contexto_rag

    return "Material não encontrado."