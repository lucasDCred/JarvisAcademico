#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from sentence_transformers import SentenceTransformer # Importa o modelo de embeddings
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Esse modelo transforma textos em vetores numéricos
modelo = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Função que gera embeddings
def gerar_embeddings(chunks):

    embeddings = modelo.encode(chunks) # Converte os textos em vetores 
    
    return embeddings