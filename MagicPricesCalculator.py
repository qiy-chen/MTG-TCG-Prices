import requests
import urllib.request
from bs4 import BeautifulSoup
import random
import traceback
import math

print("Magic Prices")
print("Uses: Calculate Deck's Budget with l'Expédition's prices")
print("Par Qi Yuan ;)")
print("Version 0.1 (29/4/21)")
a = 70
print("-"*a)

print("To read the file 'decklist.cdck' and to update the prices")
print("""The format is:
Exemple Card Name 1
Exemple Card Name 2
Exemple Card Name 3
...

DO NOT USE THOSE SPECIAL CHARACTERS: '@' or '*' !!!
Some prices may be wrong because of cards having the same name and the program picking the cheapest.
You can also use .dck file (from MTG Forge) by converting it into a useable format for the program by dropping it in the same folder, naming it 'decklistconvert.dck' and starting the program.

Press Enter to start""")
input()
def replacelist(position,x,xlist):
    xlist.pop(position)
    xlist.insert(position,x)
    return xlist

def loadcommand(option1):
    print("Loading file...")
    if option1 == "d":
        filename = "decklist.cdeck"
    elif option1 == "l":
        filename = "LandsPricing.cdeck"
    try:
        with open(filename, "r", encoding="utf-8") as savefile:
    #       savefile = open("dat.txt","w+")
            contents = savefile.read()
            contents = contents.split("\n")
            return contents
    except Exception as e:
        print("Cannot load file, quitting after Enter")
        print(e)
        input()
        quit()

def savecommand(savelist,option1):
    text = savelist
    if option1 == "d":
        filename = "DeckPricing.txt"
    elif option1 == "l":
        filename = "LandsPricing.txt"
    with open(filename, "w", encoding="utf-8") as savefile:
        savefile.write(text)
#        savefile = open("dat.txt","w+")
        savefile.close()

def convert():
    print("Loading file...")
    try:
        with open("decklistconvert.dck", "r", encoding="utf-8") as savefile:
    #       savefile = open("dat.txt","w+")
            contents = savefile.read()
            contents = contents.split("\n")
            pos = contents.index("[Main]")
            contents = contents[pos+1:]
            convertedList = []
            for i in range(len(contents)):
                item = contents[i]
                pos = item.find(" ")
                endpos = item.find("|")
                item = item[pos+1:endpos]
                convertedList.append(item)
                print("Converted " + item + " text")
            print("Done, saving...")
            text = "\n".join(convertedList)
            with open("decklist.cdeck", "w", encoding="utf-8") as savefile:
                savefile.write(text)
#               savefile = open("dat.txt","w+")
                savefile.close()
            print("Converted and saved!")
    except Exception as e:
        print("Cannot load file, quitting after Enter")
        print(e)
        input()
        quit()

def idpricebot(cardList,cardstate):
    updatedList = []
    total = 0
    cardTotal = 0
    for i in range(len(cardList)):
        cardname = cardList[i]
        if cardname.count("*") == 0:
            if cardname.count(" ") > 0:
                cardname = cardname.split(" ")
                cardname = "+".join(cardname)
            if cardname.count("@") > 0:
                pos = cardname.find("@")
                cardname = cardname[:pos]
            
            url = "https://www.expeditionjeux.com/products/search?q="+cardname+"&c=1"
            print("Searching in "+url)
            everything = requests.get(url)
            soup = BeautifulSoup(everything.content, "html.parser")
            form = soup.find_all('form', attrs = {"class": "add-to-cart-form"} )
            lowprice = 99999.9
            for i in range(len(form)):
                candidate = str(form[i])
                cardnameseparated = cardname.split("+")
                veryfier = 1
                for i in range(len(cardnameseparated)):
                    name = str(cardnameseparated[i])
                    if candidate.count(name) == 0 or candidate.count(" Art ") > 0:
                        veryfier = 0
                    if cardstate == "NM" and candidate.count("NM") == 0:
                        veryfier = 0
                if veryfier == 1:
                    pricingzone = candidate
                    pos = pricingzone.find("""<span class="regular price">CAD$ """)
                    pricing = pricingzone[pos+33:]
                    endpos = pricing.find("""</span>""")
                    pricing = pricing[:endpos]
                    try:
                        pricing = float(pricing)
                        if pricing < lowprice:
                            lowprice = pricing
                    except:
                        pass
            if lowprice == 99999.9:
                lowprice = "Not Found"
            realname = " ".join(cardnameseparated)
            print("For", realname + ":")
            print(str(lowprice)+" CAD$")
            print("-"*50)
            x = 40-len(realname)
            cardprice = str(realname + "@" + " "*x + str(lowprice))
            updatedList.append(cardprice)
            if not str(lowprice) == "Not Found":
                total += lowprice
            cardTotal += 1
    total = str(total)
    pos = int(total.find("."))
    total = total[:pos+3]
    updatedList.append("*Total: " + str(total) + " CAD$ For " + str(cardTotal) + " cards")
    return updatedList
            
                    

def main(option1):
    cardstate = "All"
    print("""Do you want to convert 'decklistconvert.dck' into a format compatible to this program?.
Attention, Commander Deck Only and the Commander is not included! (y/n)""")
    option = input()
    if option == "y":
        convert()
    print("""Do you want to accept only NM condition cards? (y/n)""")
    option = input()
    if option == "y":
        cardstate = "NM"
    url = ""
    cardList = loadcommand(option1)
    cardList = idpricebot(cardList,cardstate)
    show = "\n".join(cardList)
    print("Completed")
    print(show)
    print("Save file? (y/n)")
    option = input()
    if option == "y":
        savecommand(show,option1)
        print("Saved successfully!")
    print("Press Enter to exit")
    input()
    quit()

print("Check your deck's price or lands prices? (d/l)")
option1 = input()
if option1 == "d" or option1 == "l":
    main(option1)
else:
    print("Wrong input, please restart the program and try again")
    input()
    quit()
