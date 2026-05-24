#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import faiss # Importa FAISS para busca vetorial

import numpy as np # Importa numpy para trabalhar com vetores
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Função responsável por criar o índice vetorial
def criar_indice(embeddings):

    dimensao = len(embeddings[0]) # Descobre a dimensão dos embeddings

    indice = faiss.IndexFlatL2(dimensao) # Cria o índice FAISS

    indice.add(np.array(embeddings)) # Adiciona os embeddings no índice
   
    return indice 


# Função que busca os chunks mais relevantes
def buscar_chunks(indice, embedding_pergunta, chunks, quantidade = 3):
    
    distancias, posicoes = indice.search(np.array([embedding_pergunta]), quantidade) # Realiza a busca vetorial
    
    resultados = [] # Lista dos resultados encontrados

    # Percorre as posições encontradas
    for posicao in posicoes[0]:
        
        resultados.append(chunks[posicao]) # Adiciona o chunk correspondente
    
    return resultados # Retorna os chunks mais relevantes