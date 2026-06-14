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

client = OpenAI(base_url='https://llm.liaufms.org/v1/qwen2-5-14b-instruct-awq', api_key = 'REIkURcI7rTTqsTwlJi8MrgnKFwOiqky7Ezh7hH-l-k') # Conexão com Gemma

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

    # Data atual, hora atual e dia da semana atual
    dias_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    agora = datetime.now()
    data_hora_semana = f"{dias_semana[agora.weekday()]}, {agora.strftime('%d/%m/%Y %H:%M')}"
    

    dados_agenda = consultar_agenda() # Consulta agenda do usuário

    dados_tarefas = listar_tarefas() # Consulta tarefas do usuário

    memoria = carregar_memoria(12) # Carrega memória da IA com as 12 últimas mensagens

    contexto_rag = "" # Contexto RAG começa vazio

    #============================================================================
    # Contexto da IA
    contexto_sistema = f"""
    Você é um assistente inteligente para estudantes.

    Atual data, hora e dia da semana exata: {data_hora_semana}

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

    Quando o usuário pedir um plano de estudos, cronograma de estudos ou perguntar o que deve priorizar, responda somente:

    PLANO_ESTUDOS

    Não invente informações e seja direto ao ponto.
    """
    #============================================================================

    # Modelo de IA, Contexto da IA + memória
    resposta = client.chat.completions.create(
        model='Qwen/Qwen2.5-14B-Instruct-AWQ',
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
            messages=[{"role": "system", "content": contexto_rag_sistema}, {"role": "user", "content": pergunta}])

        mensagem = resposta_rag.choices[0].message.content # Atualiza resposta final

    # Adicionar tarefa
    elif mensagem.startswith("ADICIONAR_TAREFA:"):

        descricao = mensagem.replace("ADICIONAR_TAREFA:", "").strip() # Remove somente o comando

        mensagem = adicionar_tarefa(descricao) # Executa tarefa

    # Concluir tarefa
    elif mensagem.startswith("CONCLUIR_TAREFA:"):

        id_tarefa = int(mensagem.replace("CONCLUIR_TAREFA:", "").strip()) # Extrai ID

        mensagem = concluir_tarefa(id_tarefa) # Conclui tarefa

    # Plano de estudos
    elif mensagem.startswith("PLANO_ESTUDOS"):

        plano_estudo = f"""
        Você é um orientador de estudos e deve utilizar as seguintes informações:

        Atual data, hora e dia da semana exata: {data_hora_semana}

        Agenda do usuário:

        {dados_agenda}

        Tarefas do usuário:

        {dados_tarefas}

        Materiais disponíveis para estudo:

        {palavras_chave}

        Monte um plano de estudos objetivo, indicando prioridades e ordem de estudo.
        """

        plano_estudo = client.chat.completions.create(
            model='Qwen/Qwen2.5-14B-Instruct-AWQ',
            messages=[{"role": "system", "content": plano_estudo}, {"role": "user", "content": pergunta}])
        
        mensagem = plano_estudo.choices[0].message.content
    
    
    # Salvamento final
    salvar_log("IA", pergunta, mensagem) # Salva log

    salvar_mensagem("user", pergunta) # Salva user

    salvar_mensagem("assistant", mensagem) # Salva assistant

    print("\nGemma:", mensagem)
    print()