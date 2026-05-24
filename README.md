# README — Jarvis Acadêmico com RAG

## Descrição do Projeto

O Jarvis Acadêmico é um assistente inteligente para estudos desenvolvido em Python, utilizando um modelo de linguagem integrado com RAG (Retrieval-Augmented Generation). O sistema é capaz de consultar documentos PDF acadêmicos, responder perguntas, fazer questões, verificar respostas, gerenciar tarefas e acessar informações da agenda do usuário.

O projeto utiliza busca semântica com embeddings e recuperação vetorial para encontrar trechos relevantes dos documentos e gerar respostas contextualizadas.

# Funcionalidades

* Consulta de documentos PDF utilizando RAG
* Busca semântica por embeddings
* Geração de respostas contextualizadas
* Sistema de memória de conversa
* Gerenciamento de tarefas
* Consulta de agenda
* Sistema de logs
* Extração de palavras-chave dos documentos

# Tecnologias Utilizadas

* Python
* FAISS
* SentenceTransformers
* OpenAI SDK
* Gemma-3-12B-IT
* JSON

# Estrutura do Projeto

* dados/ → PDFs, agenda e tarefas
* ferramentas/ → funções auxiliares do sistema
* rag/ → implementação do RAG
* logs/ → histórico das interações
* IAmemoria/ → memória da IA
* main.py → código principal

# Instalação

Instale manualmente as bibliotecas necessárias:

```bash id="9u7bhj"
pip install openai
```

```bash id="ovl4k7"
pip install sentence-transformers
```

```bash id="h4s7fr"
pip install faiss-cpu
```

```bash id="t4jlwm"
pip install numpy
```

```bash id="2hhj5x"
pip install pypdf
```

```bash id="bt5f7g"
pip install torch
```

```bash id="jlwmr4"
pip install transformers
```

```bash id="z2p2j5"
pip install huggingface-hub
```

# Execução

Após instalar as bibliotecas, execute:

```bash id="r5m4m9"
python main.py
```

# Como Utilizar

Digite perguntas normalmente no terminal.

Exemplos:

* “Que dia é hoje??”
* “O que é KNN?”
* “Como funciona a fotossíntese?”
* “Quais tarefas eu tenho?”
* “Qual minha agenda de hoje?”

# Estratégia de RAG

O sistema divide os documentos em chunks de aproximadamente 120 palavras, utilizando uma sobreposição de 20 palavras entre chunks para preservar contexto.

Os chunks são transformados em embeddings vetoriais e armazenados em um índice vetorial para busca semântica.

# Lista de IAs Utilizadas

* Gemma-3-12B-IT
* Sentence Transformers — paraphrase-multilingual-MiniLM-L12-v2

# Autor

Lucas Dantas Carvalho
