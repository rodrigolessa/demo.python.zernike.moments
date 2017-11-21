# http://docs.python-requests.org/en/master/
import requests
from bs4 import BeautifulSoup

# Exemplo com authentication do GitHub
# r = requests.get('https://api.github.com/user', auth=('user', 'pass'))

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
    # Exibindo o conteúdo HTML da página, formatado corretamente
    # print(soup.prettify())
    #list(soup.children)
    # Find for span tags with Images links and descriptions
    infocard = soup.find_all('span', class_='infocard-tall')
