# Libraries for web crawler
# http://web.stanford.edu/~zlotnick/TextAsData/Web_Scraping_with_Beautiful_Soup.html
from bs4 import BeautifulSoup
# http://docs.python-requests.org/en/master/
import requests
# Managing windows files
import os.path
# I just use for a break, waiting 5 seconds until next request
import time

# Args constructor for execute on console, podendo ser obrigatórios
#a = argparse.ArgumentParser()
#a.add_argument("-p", "--image-list", required=True, help="Path to where the raw HTML file resides")
#a.add_argument("-s", "--sprites", required=True, help="Path where the sprites will be stored")

#args = vars(a.parse_args())

# Initial sets
dbUrl = 'https://pokemondb.net/pokedex/national'
imageUrl = 'https://img.pokemondb.net/sprites/red-blue/normal/'
imageFolder = 'spritesRedBlue'
imageExtension = '.png'
i = 0

def getHTML(url):
    # Navigate to site
    page = requests.get(url)
    # Try if URL respond
    if (page.status_code == 200):
        # print(page.headers['content-type']) 
        # print(page.encoding) 
        # print(page.text)
        return BeautifulSoup(page.content, 'html.parser')

def getImageLinks(url):
    # Find for 'a' tags  that contains a specific class name
    return getHTML(url).find_all('a', class_='ent-name', href=True)

def getImageName(strLink):
    return strLink.replace('/', '').replace('pokedex', '').lower()

	# if the name contains an apostrophe (such as in
	# Farfetch'd, just simply remove it)
	#parsedName = parsedName.replace("'", "")
	# if the name contains a period followed by a space
	# (as is the case with Mr. Mime), then replace it
	# with a dash
	#parsedName = parsedName.replace(". ", "-")
	# handle the case for Nidoran (female)
	#if parsedName.find(u'\u2640') != -1:
		#parsedName = "nidoran-f"
	# and handle the case for Nidoran (male)
	#elif name.find(u'\u2642') != -1:
		#parsedName = "nidoran-m"

def getPokeImages(strLink, imageNumber):
    imageZeros = '{0:0>3}'.format(imageNumber)
    # Build paths using image name
    imageName = getImageName(strLink)
    httpcurl = '{}{}{}'.format(imageUrl, imageName, imageExtension)
    physical = '{}/{}{}{}'.format(imageFolder, imageZeros
            , imageName.replace('-', '').title()
            , imageExtension)
    # ! Information
    print("downloading {}".format(imageName))
    # If do not exists in image folder
    if os.path.exists(physical):
        return
    # Get image
    r = requests.get(httpcurl)
    # If the status code is not 200, ignore the sprite
    if r.status_code != 200:
        print("downloading error {0}".format(imageName))
        return
    # Write the sprite to file
    f = open(physical, "wb")
    f.write(r.content)
    f.close()
    # Wait until next link - Avoid Push out for remote host
    time.sleep(5)

##############################################################################
# Execute web scraping
# Get all valid links from url
links = getImageLinks(dbUrl)
# Loop over all link elements
for l in links:
    i += 1
    # print(strLink.text) 
    # Extract URL from soup link 
    # print(strLink['href'])
    # Download all images
    getPokeImages(l['href'], i)