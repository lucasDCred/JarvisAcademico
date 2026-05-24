#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from openai import OpenAI # Biblioteca para conectar com a Gemma

from datetime import datetime # Biblioteca para pegar data/hora atual

from logs.logger import salvar_log # Importa escritor de logs

from IAmemoria.memoria import (salvar_mensagem, carregar_memoria) # Importa memória da IA

from ferramentas.agenda import consultar_agenda # Funções da agenda

from ferramentas.tarefas import (listar_tarefas, adicionar_tarefa, concluir_tarefa) # Funções das tarefas

from ferramentas.rag_tool import buscar_material_rag # Ferramenta RAG

from ferramentas.palavraChave import obter_palavras_chave # Ferramenta de palavras-chave
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

client = OpenAI(base_url='https://llm.liaufms.org/v1/gemma-3-12b-it', api_key='Cxt2ftLF7d3mHS2JdiFqB-eSDAQeZvFATPXPs02lV9A') # Conexão com Gemma

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

palavras_chave = obter_palavras_chave() # Carrega palavras chave dos PDFs

# Mensagem inicial
print("==== JARVIS ACADÊMICO ====")
print("Digite 'sair' para encerrar\n")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Loop principal
while True:

    pergunta = input("Você: ") # Recebe pergunta do usuário

    texto = pergunta.lower() # Tira a caixa alta da pergunta

    # Encerra programa
    if texto == "sair":
        print("Encerrando...")
        break

    # Data atual
    data_hoje = datetime.now().strftime("%d/%m/%Y")

    dados_agenda = consultar_agenda() # Consulta agenda do usuário

    dados_tarefas = listar_tarefas() # Consulta tarefas do usuário

    memoria = carregar_memoria(12) # Carrega memória da IA com as 12 últimas mensagens

    contexto_rag = "" # Contexto RAG começa vazio

    #============================================================================
    # Contexto da IA
    contexto_sistema = f"""
    Você é um assistente inteligente para estudantes.

    Hoje é {data_hoje}.

    Esta é a agenda real do usuário:

    {dados_agenda}

    Estas são as tarefas reais do usuário:

    {dados_tarefas}

    Você possui materiais de estudo sobre:

    {palavras_chave}

    Se a pergunta do usuário estiver relacionada a alguma palavra citada no material de estudo, responda imediatamente e somente:

    USAR_RAG: nome_do_arquivo.pdf

    Se o usuário pedir para voce produzir questões ou corrigir a resposta do usuário e ela tiver alguma palavra citada no material de estudo, responda imediatamente e somente:

    USAR_RAG: nome_do_arquivo.pdf

    Quando o usuário quiser adicionar uma "tarefa", responda somente neste formato:

    ADICIONAR_TAREFA: descrição da tarefa

    Quando o usuário quiser concluir uma "tarefa", responda somente neste formato:

    CONCLUIR_TAREFA: numero

    Não invente informações e seja direto ao ponto.
    """
    #============================================================================

    # Modelo de IA, Contexto da IA + memória
    resposta = client.chat.completions.create(
        model='google/gemma-3-12b-it',
        messages=[{"role": "system", "content": contexto_sistema}] + memoria + [{"role": "user", "content": pergunta}])

    mensagem = resposta.choices[0].message.content # Guarda resposta da IA

    # Se a IA decidir usar RAG
    if mensagem.startswith("USAR_RAG:"):

        contexto_rag = buscar_material_rag(pergunta, mensagem) # Busca material relevante

        # Contexto do RAG
        contexto_rag_sistema = f"""
        Você é um assistente acadêmico.

        Use SOMENTE o material abaixo para responder.

        Material encontrado:

        {contexto_rag}

        Responda de forma natural e didática.
        """

        # Segunda chamada da IA
        resposta_rag = client.chat.completions.create(
            model='google/gemma-3-12b-it',
            messages=[
                {
                    "role": "system",
                    "content": contexto_rag_sistema
                },
                {
                    "role": "user",
                    "content": pergunta
                }
            ]
        )

        mensagem = resposta_rag.choices[0].message.content # Atualiza resposta final

    # Adicionar tarefa
    elif mensagem.startswith("ADICIONAR_TAREFA:"):

        descricao = mensagem.replace("ADICIONAR_TAREFA:", "").strip() # Remove somente o comando

        mensagem = adicionar_tarefa(descricao) # Executa tarefa

    # Concluir tarefa
    elif mensagem.startswith("CONCLUIR_TAREFA:"):

        id_tarefa = int(mensagem.replace("CONCLUIR_TAREFA:", "").strip()) # Extrai ID

        mensagem = concluir_tarefa(id_tarefa) # Conclui tarefa
    
    
    # Salvamento final
    salvar_log("IA", pergunta, mensagem) # Salva log

    salvar_mensagem("user", pergunta) # Salva user

    salvar_mensagem("assistant", mensagem) # Salva assistant

    print("\nGemma:", mensagem)
    print()