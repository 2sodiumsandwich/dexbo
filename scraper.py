#!/usr/bin/python3
import requests
import httplib2
from bs4 import BeautifulSoup
import json

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

def getpokelink(query):
    s = requests.Session() #start session
    url = "https://www.google.com/search?&q=" + query.replace(" ", "+") + "+pokedex" + "+site:serebii.net" + "&ie=utf-8&oe=utf-8" #google search url
    search = s.get(url, headers=header_Get)
    
    soup = BeautifulSoup(search.text, "html.parser") #parsing html
    output = []
    for searchWrapper in soup.find_all('a'):
        url = searchWrapper.get('href')
        keyterms = ["pokedex", "serebii"]
        badkeyterms = ["google", "3dpro", "search"]
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
                link = "https://www.serebii.net/pokedex-sm/" + output[i].split("/")[-1] #change pokedex region to sm
                if(int(httplib2.Http().request(link, "HEAD")[0]['status']) < 400): #testing if link works
                    return link
                else:
                    i += 1

def pokescraper(url):
    s = requests.Session()
    page = s.get(url, headers=header_Get)

    soup = BeautifulSoup(page.text, "html.parser")
    data = {
        "id": None,
        "name": None,
        "stats": {
            "hp": None,
            "atk": None,
            "def": None,
            "spatk": None,
            "spdef": None,
            "spd": None
        },
        "abilities": None,
        "hidden": None,
        "type": None,
        "thumb": None
    }

    data["id"] = (soup.title.string).split(" ")[2] #id
    data["name"] = (soup.title.string).split(" ")[0] #name
    data["thumb"] = "http://play.pokemonshowdown.com/sprites/xyani/" + data["name"].lower() + ".gif" #thumb

    datajson = s.get("https://pokeapi.co/api/v2/pokemon/" + data["name"].lower(), headers=header_Get).json() #get json from pokeapi.co


    #abilities
    abils = []
    habils = []
    for x in range(0, len(datajson["abilities"])):
        if(datajson["abilities"][x]["is_hidden"]):
            habils.append(datajson["abilities"][x]["ability"]["name"])
        else:
            abils.append(datajson["abilities"][x]["ability"]["name"])
    data["abilities"] = abils
    data["hidden"] = habils


    #stats
    data["stats"]["spd"] = datajson["stats"][0]["base_stat"]
    data["stats"]["spdef"] = datajson["stats"][1]["base_stat"]
    data["stats"]["spatk"] = datajson["stats"][2]["base_stat"]
    data["stats"]["def"] = datajson["stats"][3]["base_stat"]
    data["stats"]["atk"] = datajson["stats"][4]["base_stat"]
    data["stats"]["hp"] = datajson["stats"][5]["base_stat"]

    #types
    types = []
    for x in range(0, len(datajson["types"])):
        types.append(datajson["types"][x]["type"]["name"])
    data["type"] = types

    return json.dumps(data)