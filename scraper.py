import requests
import httplib2
from bs4 import BeautifulSoup
import json
from json import dumps
from xmljson import badgerfish as bf
import xmltodict
from xml.etree.ElementTree import fromstring

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

def getlink(query, queryterms, keyterms, badkeyterms):
    s = requests.Session() #start session
    url = "https://www.google.com/search?&q="  + query.replace(" ", "%20")
    for x in queryterms: url += "+" + x  
    url += "&ie=utf-8&oe=utf-8"     
    search = s.get(url, headers=header_Get) #parsing html

    soup = BeautifulSoup(search.text, "html.parser")
    output = []
    for searchWrapper in soup.find_all('a'):
        url = searchWrapper.get('href')
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
                if(int(httplib2.Http().request(output[i], "HEAD")[0]['status']) < 400): #testing if link works
                    return output[i]
                else:
                    i += 1

def pokescraper(url):
    url = "https://www.serebii.net/pokedex-sm/" + url.split("/")[-1]
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
    data["thumb"] = 'http://play.pokemonshowdown.com/sprites/xyani/' + data["name"].lower() + '.gif' #thumb
    print(data["id"].lower().lstrip("0").lstrip("#"))
    try:
        datajson = s.get("https://pokeapi.co/api/v2/pokemon/" + data["id"].lower().lstrip("#").lstrip("0"), headers=header_Get).json() #get json from pokeapi.co
    except:
        return False

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

def getLegos(url):
    s = requests.Session()
    page = s.get(url, headers=header_Get)

    soup = BeautifulSoup(page.text, "html.parser")
    data = {
        "id": None,
        "year": None,
        "name": None,
        "pieces": None,
        "thumb": None,
        "priceUS": None,
        "brickUrl": None
    }

    data["id"] = (soup.title.string).split(" ")[0][:-1] #id of set 

    with open("auth.json", "r") as read_file:
        credentials = json.load(read_file)
    API_ENDPOINT = "https://brickset.com/api/v2.asmx/login?apiKey=" + credentials["bsapikey"] + "&username=" + credentials["bsuser"]+ "&password=" + credentials["bspw"]
    r = requests.get(url = API_ENDPOINT)
    USERHASH = bf.data(fromstring(r.content))[list(bf.data(fromstring(r.content)))[0]]["$"] #requesting userhash from api/login
    
    API_ENDPOINT = "https://brickset.com/api/v2.asmx/getSets?apiKey=" + credentials["bsapikey"] + "&userHash=\"" + USERHASH + "\"&query=" + data["id"] + "&theme=&subtheme=&setnumber=&year=&owned=&wanted=&orderby=&pagesize=&pagenumber=&username="

    r = requests.get(url = API_ENDPOINT)
    SETDATA = dict(dict(xmltodict.parse(r.content)["ArrayOfSets"])['sets'])
    data["year"] = SETDATA["year"]
    data["name"] = SETDATA["name"]
    data["pieces"] = SETDATA["pieces"]
    data["thumb"] = SETDATA["thumbnailURL"].replace("small","large")
    data["priceUS"] = SETDATA["USRetailPrice"]
    data["brickUrl"] = SETDATA["bricksetURL"]
    
    return json.dumps(data)