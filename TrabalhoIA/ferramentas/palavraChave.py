#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import os # Biblioteca para acessar arquivos

from rag.carregadorPDF import carregar_pdf # Função que carrega PDF
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def obter_palavras_chave():

    palavras_chave = {} # Palavra chave de cada PDF

    # Percorre todos os arquivos da pasta
    for arquivo in os.listdir("dados/documentos"):

        # Verifica se é PDF
        if arquivo.endswith(".pdf"):

            print(f"Analisando palavras chave: {arquivo}")

            # Caminho completo do PDF
            caminho = f"dados/documentos/{arquivo}"

            # Carrega texto do PDF
            texto = carregar_pdf(caminho)

            # Divide em palavras
            palavras = texto.lower().split()

            palavras_filtradas = [] # Lista temporária

            # Percorre palavras do PDF
            for p in palavras:

                # Deixa apenas palavras maiores que 4 letras
                if len(p) > 4:
                    palavras_filtradas += [p] # Adiciona ao final da lista

            # Remove palavras repetidas
            palavras_unicas = list(set(palavras_filtradas))

            # Pega apenas somente N palavras
            N_palavras = palavras_unicas[:50]

            # Salva
            palavras_chave[arquivo] = N_palavras

    return palavras_chave