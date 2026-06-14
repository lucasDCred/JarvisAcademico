#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from pypdf import PdfReader # Importa a biblioteca que lê PDFs
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Função que carregar o PDF
def carregar_pdf(caminho_pdf):
    
    texto = "" # Variável que irá armazenar todo o texto do PDF
   
    pdf = PdfReader(caminho_pdf) # Abre o PDF

    # Percorre todas as páginas do PDF
    for pagina in pdf.pages:
        
        conteudo = pagina.extract_text() # Extrai o texto da página

        # Verifica se conseguiu extrair algo
        if conteudo:
            
            texto += conteudo + "\n" # Adiciona o texto na variável principal

    # Retorna todo o texto extraído
    return texto