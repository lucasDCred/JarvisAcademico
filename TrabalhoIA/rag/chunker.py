def dividir_chunks(texto, tamanho = 120, sobreposicao = 20): # Função responsável por dividir o texto em partes menores (por palavras)

    chunks = [] # Lista que armazenará os chunks
    
    palavras = texto.split() # Separa o texto em palavras
   
    inicio = 0 # Posição inicial

    # Percorre a lista de palavras
    while inicio < len(palavras):

        fim = inicio + tamanho # Define o fim do chunk
        
        chunk_palavras = palavras[inicio:fim] # Pega o pedaço de palavras
       
        chunk = " ".join(chunk_palavras) # Junta de volta em texto
       
        chunks.append(chunk) # Adiciona o chunk na lista
       
        inicio += tamanho - sobreposicao # Avança com sobreposição

    # Retorna todos os chunks
    return chunks