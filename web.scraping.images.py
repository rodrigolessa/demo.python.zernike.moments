# http://docs.python-requests.org/en/master/
import requests
# http://web.stanford.edu/~zlotnick/TextAsData/Web_Scraping_with_Beautiful_Soup.html
from bs4 import BeautifulSoup
# https://docs.python.org/3/library/argparse.html
import argparse
# Manipulando arquivos
import os.path
import time

# Construtor de algumentos para execução no console, podendo ser obrigatórios
#a = argparse.ArgumentParser()
#a.add_argument("-p", "--image-list", required=True, help="Path to where the raw HTML file resides")
#a.add_argument("-s", "--sprites", required=True, help="Path where the sprites will be stored")

#args = vars(a.parse_args())

fileExtension = 'jpg'

# Exemplo com authentication do GitHub
# r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
# Obtendo o HTML da página
page = requests.get('https://pokemondb.net/pokedex/national')

print('Verificando se o endereço está correto!')
print('Status code')
print(page.status_code)

if (page.status_code == 200):
    print('Headers')
    print(page.headers['content-type'])
    # print('Encoding')
    # print(page.encoding)
    # print('Text')
    # print(page.text)
    # print('Content')
    # print(page.content)
    # Analisando o conteúdo da página com a Biblioteca BeautifulSoup
    # https://imasters.com.br/desenvolvimento/aprendendo-sobre-web-scraping-em-python-utilizando-beautifulsoup/?trace=1519021197&source=single
    soup = BeautifulSoup(page.content, 'html.parser')
    # list(soup.children)
    # Exibindo o conteúdo HTML da página, formatado corretamente
    # print(soup.prettify())
    # Find for span tags with Images links and descriptions
    #infocard = soup.find_all('span', class_='infocard-tall')
    links = soup.find_all('a', class_='ent-name', href=True)
    # Loop over all link elements
    for l in links:
        # Tratar os nomes das imagens
        name = l['href'].replace('/pokedex/', '')
        # print(l.text)
        # print(l['href'])
        # Verificar se a imagem já existe no diretório
        if (os.path.exists('sprites/%s.%s' % (name, fileExtension))):
            print("Arquivo %s já existe!" % (name))
            continue
        # construct the URL to download the sprite
        print("[x] downloading %s" % (name))
        imageUrl = "https://img.pokemondb.net/artwork/%s.%s" % (name, fileExtension)
        r = requests.get(imageUrl)
        # if the status code is not 200, ignore the sprite
        if r.status_code != 200:
            print("[x] error downloading %s" % (name))
            continue
        # write the sprite to file
        f = open("%s/%s.%s" % ('sprites', name.lower(), fileExtension), "wb")
        f.write(r.content)
        f.close()
        # Wait until next link - Foi forçado o cancelamento de uma conexão existente pelo host remoto
        time.sleep(5)