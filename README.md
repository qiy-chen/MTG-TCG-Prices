# MTG-TCG-Prices

Created as a personnal learning project.
Written in Python 3

Version 0.1

Fetch the lowest price of each card of Magic:The Gathering of a list from a vendor's website (currently l'Expédition).

## The program is divided into three main parts:

1. A main user console interface

2. A set of function to load and save user lists

3. A set of function to request raw HTML data and to extract the relevant information.


## Instructions:

Your list must be named **"decklist.cdeck"** (edit the file extension) and be **in the program's root**.

If you want to convert your decklist from MTG Forge (.dck), it must be named **"decklistconvert.dck"** and be **in the program's root**.

Be sure that you have Python 3 installed in your computer.

Open **MagicPricesCalculator.py** and you are ready to go!

## Limits

Being my first program manipulating HTML data, it has unfortunately some limitations.

It calculates only the price of one unit per card (multiple instances of a card are counted as one).

For performance reasons, it only fetches the first page of the search result.

Only one vendor is available for now, more will be added later.

The file opening system is rigid, requiring specific names to detect the required files.
