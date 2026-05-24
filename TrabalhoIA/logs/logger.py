#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import json # Biblioteca JSON

from datetime import datetime # Biblioteca para pegar data/hora atual
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

nome_arquivo = datetime.now().strftime("conversa %ddia - %Hh%Mmin.json") # Nome do arquivo json da atual sessão

caminho_log = f"logs/{nome_arquivo}" # Caminho do novo arquivo de log json


def salvar_log(tipo, entrada, saida): # Função para salvar a interação no json

    #interação
    log = {
        "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "tipo": tipo,
        "entrada": str(entrada),
        "saida": str(saida)
    }   


    # Lê logs existentes
    try:
        with open(caminho_log, "r", encoding = "utf-8") as arquivo:
            logs = json.load(arquivo)
    except:
        logs = []


    logs.append(log) # adiciona ao final da lista


    # Salva novamente
    with open(caminho_log, "w", encoding = "utf-8") as arquivo:
        json.dump(logs, arquivo, ensure_ascii = False, indent = 4)