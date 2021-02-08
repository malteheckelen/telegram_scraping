# Get Telegram Data from Seed Channel

More detailed explanation to follow.

**TO DO**:

* Some uncleared issues with recursion: sometimes, it just stops after a some layers and you have to restart manually
* Structure telegram_functions.py better
* Remove analysis scripts and Notebooks


This repository contains scripts for interacting with the Telegram API. For my own use-case, I wanted to traverse the forward network of certain Telegram channels from the German Corona-sceptic sphere. 

For this, I wrote a little function that allows me to start with a seed channel and, after getting its messages and their metadata, also get the data from forwarded channels. This repeats recursively until no more new forwards are found or you stop it.
