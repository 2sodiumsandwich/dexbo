#!/usr/bin/python3
import requests
import httplib2
from bs4 import BeautifulSoup

#set HTTP header
header_Get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

def getlink(query):
    s = requests.Session() #start session
    url = "https://www.google.com/search?&q=" + query.replace(" ", "+") + "+pokemon" + "+site:serebii.net" + "&ie=utf-8&oe=utf-8" #google search url
    search = s.get(url, headers=header_Get)
    
    soup = BeautifulSoup(search.text, "html.parser") #parsing html
    output = []
    for searchWrapper in soup.find_all('a'):
        url = searchWrapper.get('href')
        keyterms = ["pokedex", "serebii"]
        badkeyterms = ["google", "3dpro"]
        if(url is not None and all(x in url for x in keyterms) and not any(y in url for y in badkeyterms)): #looking for links
            output.append(url)
            
    if(not output):
        print("No results")
        return False
    else:
        i = 0
        while(True):
            if(i >= len(output)):
                print("No results")
                return False
            else:
                link = output[i].split("pokedex-")[0] + "pokedex-sm" + output[i].split("pokedex-")[1][2:] #change pokedex to sm
                if(int(httplib2.Http().request(link, "HEAD")[0]['status']) < 400): #testing if link works
                    return link
                else:
                    i += 1

def pokescraper():
    return 0