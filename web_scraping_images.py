# Libraries for web crawler
# http://docs.python-requests.org/en/master/
import requests
# Managing url
from urllib.parse import urlparse
# http://web.stanford.edu/~zlotnick/TextAsData/Web_Scraping_with_Beautiful_Soup.html
from bs4 import BeautifulSoup
# https://docs.python.org/3/library/argparse.html
import argparse
# Managing windows files
import os.path
# I just use for a break, waiting 5 seconds until next request
import time
# Regex
import re

# Args constructor for execute on console, podendo ser obrigatórios
#a = argparse.ArgumentParser()
#a.add_argument("-p", "--image-list", required=True, help="Path to where the raw HTML file resides")
#a.add_argument("-s", "--sprites", required=True, help="Path where the sprites will be stored")

#args = vars(a.parse_args())

# Initial sets
baseUrl = 'https://pokemondb.net'
baseUrlFolder = '/pokedex'
baseUrlFolderImage = '/artwork'
imageFolder = 'sprites'
imageExtension = '.jpg'
i = 0

def getHTML(url):
    # Examples with GitHub authentication # r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
    # Navigate to site
    page = requests.get(url)
    # print('Confirm id URL is correct!')
    # print('Status code: %s' % page.status_code)
    # Try if URL respond
    if (page.status_code == 200):
        # print(page.headers['content-type']) # print(page.encoding) # print(page.text) # print(page.content)
        # Get HTML using BeautifulSoup library # https://imasters.com.br/desenvolvimento/aprendendo-sobre-web-scraping-em-python-utilizando-beautifulsoup/?trace=1519021197&source=single
        return BeautifulSoup(page.content, 'html.parser')

# Find for 'a' tags  that contains a specific class name
def getPokeLinks(url):
    # Get the HTML soup # list(soup.children) # print(soup.prettify())
    return getHTML(url).find_all('a', class_='ent-name', href=True)

def getPokeName(strLink):
    return strLink.replace('%s/' % baseUrlFolder, '').lower()

def getPokeImages(strLink):
    # Confirm the names of images
    name = getPokeName(strLink)
    # ! Information
    print("[%s/%s] downloading %s" % (i, total, name))
    # construct the URL to download the sprite
    # imageUrl = "https://img.pokemondb.net/artwork/%s.%s" % (name, imageExtension)
    # Get all images tags
    # Using Regex https: // docs.python.org / 3 / library / re.html
    images = getHTML(baseUrl + strLink).findAll('img', {'src': re.compile('.*artwork.*' + imageExtension)})
    # Loop over all images
    for img in images:
        # Extract image url
        imgUrl = img['src']
        imgPath = urlparse(imgUrl).path
        # Extract image name
        imgName = imgPath.replace('%s/' % baseUrlFolderImage, '')
        # Consider only Jpeg images
        if imgName[-4:] != imageExtension:
            continue
        # If do not exists in image folder
        if os.path.exists('%s/%s' % (imageFolder, imgName)):
            # print("The file %s already exists!" % (imgName))
            continue
        # Get image
        r = requests.get(imgUrl)
        # If the status code is not 200, ignore the sprite
        if r.status_code != 200:
            print("[x] downloading error %s" % (imgUrl))
            continue
        # Write the sprite to file
        f = open("%s/%s" % (imageFolder, imgName), "wb")
        f.write(r.content)
        f.close()
        # Wait until next link - Avoid Push out for remote host
        #time.sleep(5)

##############################################################################
# Execute web scraping
# Get all valid links from url
links = getPokeLinks('%s%s/national' % (baseUrl, baseUrlFolder))
# Images total
total = len(links)
# Loop over all link elements
for l in links:
    # increment
    i += 1
    # Extract URL from soup link # print(strLink.text) # print(strLink['href'])
    # TODO: Validate link url
    # Download all images
    getPokeImages(l['href'])