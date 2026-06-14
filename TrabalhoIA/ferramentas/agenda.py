#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import json # Biblioteca JSON
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def consultar_agenda():
    
    # Abre o arquivo da agenda
    with open("dados/dadosAgenda.json", "r", encoding = "utf-8") as arquivo:
        agenda = json.load(arquivo)

    texto = ""

    for item in agenda:

        # Aula semanal
        if item["tipo"] == "aula":
            texto += f"Aula: {item['dia']} - {item['disciplina']} ({item['inicio']} às {item['fim']})\n"

        # Prova com data específica
        elif item["tipo"] == "prova":
            texto += f"Prova: {item['data']} - {item['disciplina']} - {item['nome']} ({item['inicio']} às {item['fim']})\n"

        # Trabalho com data específica
        elif item["tipo"] == "trabalho":
            texto += f"Trabalho: {item['data']} - {item['disciplina']} - {item['nome']} (até {item['fim']})\n"

        # Atividade com data específica
        elif item["tipo"] == "atividade":
            texto += f"Atividade: {item['data']} - {item['disciplina']} - {item['nome']} (até {item['fim']})\n"

    return texto