#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import json # Biblioteca JSON
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

caminho = "IAmemoria/memoria.json"  # Caminho do arquivo de memória


def salvar_mensagem(role, content):  # Salva mensagens no histórico da IA para ela mesma consultar

    # Tenta carregar memória existente
    try:
        with open(caminho, "r", encoding = "utf-8") as arquivo:
            mensagens = json.load(arquivo)

    # Se o arquivo não existir, cria lista vazia
    except:
        mensagens = []

    # Adiciona nova mensagem ao histórico
    mensagens.append({"role": role, "content": content})

    # Atualiza o arquivo de memória
    with open(caminho, "w", encoding = "utf-8") as arquivo:
        json.dump(mensagens, arquivo, ensure_ascii = False, indent = 4)


def carregar_memoria(numero): # Carrega as últimas N mensagens salvas

    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            memoria = json.load(arquivo)

        return memoria[-numero:]

    # Retorna lista vazia se não existir memória
    except:
        return []