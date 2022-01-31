import requests
import urllib.request
from bs4 import BeautifulSoup
import random
import traceback
import math
import os
#To get the correct path directory
os.chdir(os.path.dirname(__file__))

#Head Intro
print("Magic Prices")
print("Uses: Calculate Deck's Budget with l'Expédition's prices")
print("By Qi Yuan")
print("Version 0.1 (29/4/21)")
a = 70
print("-"*a)

print("To read the file 'decklist.cdck' and to update the prices")
print("""The format is:
Example Card Name1
Example Card Name2
Example Card Name3
...

DO NOT USE THOSE SPECIAL CHARACTERS: '@' or '*' !!!
Some prices may be wrong because of cards having the same name and the program picking the cheapest.
You can also use .dck file (from MTG Forge) by dropping the .dck file in the same folder as the program, naming it 'decklistconvert.dck' and starting the program.

Press Enter to start""")
input()
#A simple function to replace any element in a list with another
def replacelist(position,x,xlist):
    xlist.pop(position)
    xlist.insert(position,x)
    return xlist

#A function to load a file
#-option1: choose to load a custom decklist("d") or a default lands only list("l") at the program's root
#Return the content of the file as a list
def loadcommand(option1):
    print("Loading file...")
    if option1 == "d":
        filename = "decklist.cdeck"
    elif option1 == "l":
        filename = "LandsPricing.cdeck"
    try:
        with open(os.getcwd()+"\\"+filename, "r", encoding="utf-8") as savefile:
    #       savefile = open("dat.txt","w+")
            contents = savefile.read()
            contents = contents.split("\n")
            return contents
    except Exception as e:
        print("Cannot load file, quitting after Enter")
        print(e)
        input()
        quit()

#Function to save the list
#-option1: choose to save a decklist("d") or a land only list("l") at the program's root
def savecommand(savelist,option1):
    text = savelist
    if option1 == "d":
        filename = "DeckPricing.txt"
    elif option1 == "l":
        filename = "LandsPricing.txt"
    with open(os.getcwd()+"\\"+filename, "w", encoding="utf-8") as savefile:
        savefile.write(text)
#        savefile = open("dat.txt","w+")
        savefile.close()

#Function to convert a file named decklistconvert.dck (format used by MTG Forge for deck lists) into a useable file for this program
def convert():
    print("Loading file...")
    try:
        with open(os.getcwd()+"\\"+"decklistconvert.dck", "r", encoding="utf-8") as savefile:
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
            with open(os.getcwd()+"\\"+"decklist.cdeck", "w", encoding="utf-8") as savefile:
                savefile.write(text)
#               savefile = open("dat.txt","w+")
                savefile.close()
            print("Converted and saved!")
    except Exception as e:
        print("Cannot load file, quitting after Enter")
        print(e)
        input()
        quit()

#Function to fetch prices of cards in a list
#-cardstate: Choose NM condition only or every condition
#-cardList: list of cards
#-return an upgraded list with prices
def idpricebot(cardList,cardstate):
    updatedList = []
    total = 0
    cardTotal = 0
#For each element, assign the name to cardname.
    for i in range(len(cardList)):
        cardname = cardList[i]
        if cardname.count("*") == 0:
            #Convert blank space into "+"
            if cardname.count(" ") > 0:
                cardname = cardname.split(" ")
                cardname = "+".join(cardname)
            #Take only the String before "@"
            if cardname.count("@") > 0:
                pos = cardname.find("@")
                cardname = cardname[:pos]
            
            #Search HTML content in the first page of result
            url = "https://www.expeditionjeux.com/products/search?q="+cardname+"&c=1"
            print("Searching in "+url)
            
            #Raw HTML data in everything
            everything = requests.get(url)
            #Raw HTML data into BeautifulSoup Object
            soup = BeautifulSoup(everything.content, "html.parser")
            #Determine if the card is in stock for each card found in the HTML
            form = soup.find_all('form', attrs = {"class": "add-to-cart-form"} )
            #Set a temporary value threshold for the lowest price available
            lowprice = 99999.9
            for i in range(len(form)):
                #Assign card name to candidate
                candidate = str(form[i])
                #Assign split card name to cardnameseparated
                cardnameseparated = cardname.split("+")
                #Set up a veryfier for the card name. Send false if it find prohibited elements (such as disqualifying word) or no "NM" condition if cardstate is "NM"
                veryfier = 1
                for i in range(len(cardnameseparated)):
                    name = str(cardnameseparated[i])
                    if candidate.count(name) == 0 or candidate.count(" Art ") > 0:
                        veryfier = 0
                    if cardstate == "NM" and candidate.count("NM") == 0:
                        veryfier = 0
                #Set the price of the card if it passes the verification and it is the current lowest price.
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
            #Set a negative result if no eligible price have been found
            if lowprice == 99999.9:
                lowprice = "Not Found"
            #Assign the correctly formated name of the card to realname
            realname = " ".join(cardnameseparated)
            #Print the state of the card
            print("For", realname + ":")
            print(str(lowprice)+" CAD$")
            print("-"*50)
            x = 40-len(realname)
            #Add the card to the updated list of cards
            cardprice = str(realname + "@" + " "*x + str(lowprice))
            updatedList.append(cardprice)
            #Count the total of card if eligible and total of cards analyzed
            if not str(lowprice) == "Not Found":
                total += lowprice
            cardTotal += 1
    total = str(total)
    pos = int(total.find("."))
    total = total[:pos+3]
    updatedList.append("*Total: " + str(total) + " CAD$ For " + str(cardTotal) + " cards")
    return updatedList
            
                    
#Main Console user interface
def main(option1):
    cardstate = "All"
    
    #Ask if user want to convert file
    print("""Do you want to convert 'decklistconvert.dck' into a format compatible to this program?(y/n)""")
    option = input()
    if option == "y":
        convert()
        
    #Ask if user want to accept only cards in Near Mint condition.
    print("""Do you want to accept only NM condition cards? (y/n)""")
    option = input()
    if option == "y":
        cardstate = "NM"
    url = ""
    cardList = loadcommand(option1)
    cardList = idpricebot(cardList,cardstate)
    
    #Print the result to the console in a properly formatted list
    show = "\n".join(cardList)
    print("Completed")
    print(show)
    print("Save file? (y/n)")
    option = input()
    #Save file if wanted
    if option == "y":
        savecommand(show,option1)
        print("Saved successfully!")
    print("Press Enter to exit")
    input()
    quit()

#Main program executing the code
print("Check your deck's price or lands prices? (d/l)")
option1 = input()
if option1 == "d" or option1 == "l":
    main(option1)
else:
    print("Wrong input, please restart the program and try again")
    input()
    quit()
