#!/usr/bin/python

import platform
import subprocess
import datetime
import tkinter
import requests
import json
import time
from geopy.geocoders import Nominatim
from tkinter import *
from tkinter import messagebox

#set tkinter gui
root = Tk()
root.title('PROYEK TOS')

width = 700
height = 700
root.geometry(str(width)+"x"+str(height))

#funcs
def getDate():
    date = datetime.datetime.today()
    msg = date.strftime("%d %B %Y %H:%M")
    return msg

def setLocation(location):
    #get location information
    geolocator = Nominatim(user_agent="PROYEK TOS")
    location = geolocator.geocode(location)
    long = str(location.longitude)
    lat = str(location.latitude)

    #weather api request
    api = "e9618ba28d1f62cad377c1cc274a0e5a"
    url = "https://api.openweathermap.org/data/2.5/weather?lat="+lat+"&lon="+long+"&appid="+api
    response = requests.get(url)
    data = response.json()
    weather = data['weather'][0]['main']+" - "+data['weather'][0]['description']
    lWeather = Label(root, text=weather, justify=LEFT).grid(row=4,column=0,sticky="W")

def getItemName(item, itemName):
    i = 0
    if item != 0:
        while True:
            if itemName['items'][i]['id'] == item:
                name = itemName['items'][i]['localized_name']
                return name
            else:
                i += 1
    else:
        return "No Item"

def getGame(inp):
    #profile
    profile_url = 'https://api.opendota.com/api/players/'+inp
    response = requests.get(profile_url)
    dataProfile = response.json()
    lProfile = Label(root, text='PROFILE DATA', justify=LEFT).grid(column=0,sticky="W")
    lName = Label(root, text='Name          : {}'.format(dataProfile['profile']['personaname']), justify=LEFT).grid(column=0,sticky="W")
    lUrl = Label(root, text='Profile url    : {}'.format(dataProfile['profile']['profileurl']), justify=LEFT).grid(column=0,sticky="W")
    lmmr = Label(root, text='MMR            : {}'.format(dataProfile['mmr_estimate']['estimate']), justify=LEFT).grid(column=0,sticky="W")
    lSpace = Label(root, text='').grid(column=0)

    #get recent matches
    match_url = 'https://api.opendota.com/api/players/'+inp+'/recentMatches'
    response = requests.get(match_url)
    dataMatch = response.json()
    m_id = dataMatch[0]['match_id']

    #get match data
    item_url = "https://api.opendota.com/api/matches/"+str(m_id)
    response = requests.get(item_url)
    dataItem = response.json()

    #get item names
    name_url = "https://raw.githubusercontent.com/joshuaduffy/dota2api/master/dota2api/ref/items.json"
    response = requests.get(name_url)
    itemName = response.json()

    #get heroes name
    hero_url = "https://api.opendota.com/api/heroes"
    response = requests.get(hero_url)
    heroName = response.json()

    lMatch = Label(root, text='MATCH DATA', justify=LEFT).grid(column=0,sticky="W")

    #set hero name
    hero_id = dataMatch[0]['hero_id']
    i = 0
    while True:
        if heroName[i]['id'] == 'undefined':
            i += 1
        else:
            id = heroName[i]['id']
        if id == hero_id:
            hero_name = heroName[i]['localized_name']
            break
        else:
            i += 1

    #get user's match data
    for i in range(10):
        if str(dataItem['players'][i]['account_id']) == inp:
            item1 = dataItem['players'][i]['item_0']
            item2 = dataItem['players'][i]['item_1']
            item3 = dataItem['players'][i]['item_2']
            item4 = dataItem['players'][i]['item_3']
            item5 = dataItem['players'][i]['item_4']
            item6 = dataItem['players'][i]['item_5']
            bp1 = dataItem['players'][i]['backpack_0']
            bp2 = dataItem['players'][i]['backpack_1']
            bp3 = dataItem['players'][i]['backpack_2']
            if dataItem['players'][i]['win'] == 1:
                win = 'Win'
            else:
                win = 'Lose'
            if dataItem['players'][i]['isRadiant'] == True:
                team = 'Radiant'
            else:
                team = 'Dire'
            text = "Recent Match Id: "+str(dataItem['match_id'])+"\nTeam: "+team+"\nHero: "+hero_name+"\nCondition: "+win+"\nKill: "+str(dataItem['players'][i]['kills'])+"\nDeaths: "+str(dataItem['players'][i]['deaths'])+"\nAssists: "+str(dataItem['players'][i]['assists'])+"\nLast hits: "+str(dataItem['players'][i]['last_hits'])+"\nDenies: "+str(dataItem['players'][i]['denies'])+"\nGPM: "+str(dataItem['players'][i]['gold_per_min'])+"\nXPM: "+str(dataItem['players'][i]['benchmarks']['xp_per_min']['raw'])
            Label(root,text=text,justify=LEFT).grid(column=0,sticky="W")
            break
    
    #set item name
    item1 = getItemName(item1, itemName)
    item2 = getItemName(item2, itemName)
    item3 = getItemName(item3, itemName)
    item4 = getItemName(item4, itemName)
    item5 = getItemName(item5, itemName)
    item6 = getItemName(item6, itemName)
    bp1 = getItemName(bp1, itemName)
    bp2 = getItemName(bp2, itemName)
    bp3 = getItemName(bp3, itemName)

    text = "Item 1: "+item1+"\nItem 2: "+item2+"\nItem 3: "+item3+"\nItem 4: "+item4+"\nItem 5: "+item5+"\nItem 6: "+item6
    Label(root,text=text,justify=LEFT).grid(column=0,sticky="W")
    text = "Backpack Item 1: "+bp1+"\nBackpack Item 2: "+bp2+"\nBackpack Item 3: "+bp3
    Label(root,text=text,justify=LEFT).grid(column=0,sticky="W")

#entry widgets
eLocation = Entry(root)
eInput = Entry(root)

#ui (grid)
lDate = Label(root, text='Date      : {}'.format(getDate()), justify=LEFT).grid(column=0,sticky="W")
lSystem = Label(root, text='System  : {} {}'.format(platform.system(),platform.machine()), justify=LEFT).grid(column=0,sticky="W")

lLocation = Label(root, text='Your Location: ', justify=LEFT).grid(column=0,sticky="W")
eLocation.grid(column=0,sticky="W")
btnLocation = Button(root, text="Set Location", command=lambda: setLocation(eLocation.get())).grid(row=3,column=1,sticky="W")
lSpace = Label(root, text='').grid(column=0)
lSpace = Label(root, text='').grid(column=0)

lInfo = Label(root, text='Insert Dota\'s account id / friend id: ').grid(column=0,sticky="W")
eInput.grid(column=0,sticky="W")
btnSubmit = Button(root, text="See your game information", command=lambda: getGame(eInput.get())).grid(row=7,column=1,sticky="W")
lSpace = Label(root, text='').grid(column=0)

root.mainloop()