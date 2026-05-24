#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import json # Biblioteca JSON
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

arquivo = "dados/dadosTarefas.json"  # Caminho do arquivo JSON onde as tarefas são armazenadas


def carregar_tarefas():  # Carrega todas as tarefas salvas no JSON
    with open(arquivo, "r", encoding = "utf-8") as f:
        return json.load(f)


def salvar_tarefas(tarefas):  # Salva a lista de tarefas no arquivo JSON

    # Sobrescreve o arquivo com as tarefas atualizadas
    with open(arquivo, "w", encoding = "utf-8") as f:
        json.dump(tarefas, f, indent = 4, ensure_ascii = False)


def listar_tarefas():  # Gera um texto formatado com todas as tarefas
    tarefas = carregar_tarefas()

    texto = ""

    # Percorre todas as tarefas cadastradas
    for tarefa in tarefas:

        # Define o status da tarefa
        status = "Concluída" if tarefa["concluida"] else "Pendente"

        # Adiciona tarefa formatada ao texto final
        texto += f"{tarefa['id']} - {tarefa['descricao']} [{status}]\n"

    return texto


def adicionar_tarefa(descricao):  # Adiciona uma nova tarefa ao sistema
    tarefas = carregar_tarefas()

    # Gera ID baseado na quantidade atual de tarefas
    novo_id = len(tarefas) + 1

    # Cria estrutura da nova tarefa
    nova_tarefa = {"id": novo_id, "descricao": descricao, "concluida": False}

    # Adiciona tarefa na lista
    tarefas.append(nova_tarefa)

    # Salva alterações no JSON
    salvar_tarefas(tarefas)

    return f"Tarefa '{descricao}' adicionada com sucesso."


def concluir_tarefa(id_tarefa):  # Marca uma tarefa como concluída
    tarefas = carregar_tarefas()

    # Procura tarefa pelo ID
    for tarefa in tarefas:

        # Verifica se o ID corresponde
        if tarefa["id"] == id_tarefa:

            # Marca tarefa como concluída
            tarefa["concluida"] = True

            # Salva alterações
            salvar_tarefas(tarefas)

            return f"Tarefa '{tarefa['descricao']}' concluída."

    # Retorna mensagem caso a tarefa não exista
    return "Tarefa não encontrada."