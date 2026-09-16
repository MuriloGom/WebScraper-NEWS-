import time  # Importa a biblioteca time, usada para controlar pausas e temporização.
import schedule  # Importa a biblioteca schedule, usada para agendar tarefas.
import requests
from bs4 import BeautifulSoup
from email_sender import enviar_email

url = "https://g1.globo.com/"
def buscar_noticias():
    resposta = requests.get(url)
    resposta.raise_for_status()
    soup = BeautifulSoup(resposta.text,"html.parser")
    noticias = soup.select("div.feed-post-body-title")
    resultados = []
    for noticia in noticias:
        titulo = noticia.get_text(strip=True)
        a = noticia.find("a")
        if a and a.get("href"):
            link = a.get("href")
        resultados.append({
            "titulo": titulo,
            "link": link
        })
    return resultados
noticias = buscar_noticias()
print("Notícias encontradas:\n")
for noticia in noticias:
    print("Título:", noticia["titulo"])
    print("Link:", noticia["link"])
    print()
    
enviar_email(noticias)
#schedule.every().day.at("12:00").do(buscar_noticias)  # Agenda a execução da função buscar_noticias todos os dias às 12:00.
#while True:  # Laço infinito para manter o script ativo.
   #schedule.run_pending()  # Verifica se há tarefas agendadas para executar.
   #time.sleep(1)  # Pausa de 1 segundo para não sobrecarregar o processador.