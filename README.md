Class project for transforming the CSGO item trading experience into a more professional experience akin to a stock trading app. The Steam Market Predictor will be utilizing a Discord bot for its current iteration as Discord is a platform familiar with those who frequent the Steam Marketplace. 

# How to Setup: #
1. Make sure you have Docker installed, if not download from https://docs.docker.com/get-docker/ .
2. Copy the repo
3. Change Directory to /SMP/SMP
4. Download the requirements with ```pip install -r requirements.txt``` (incase it doesn't work, download the missing packages)
5. Add the token to /SMP/SMP/token.txt


# How to Run: #
1. Change Directory to /SMP/steam-marketplace-api and run ```docker compose up -d``` (-d makes docker run in the background, daemon mode)
2. Change Directory to /SMP/SMP
3. Run ```python bot.py```
4. In discord use !syncall 
5. You can now use the supplied slash commands

**NOTE:** use ```docker compose down``` to end docker when you are done

# Commands #

## /getitemhistory ##

**Description** 

  Returns the item's current price, price history in a list, and larger price histroy in a graph

**Parameters** 

  Name: name of CSGO Item, 
  APPID: game's steam ID (CSGO as default parameter), 
  Wear: 5 item qualities of the CSGO weapon skin that can be chosen from (required for weapons, not used for cases)
  
### Example 1 ###

  ***Name:*** P90 | Asiimov
  ***Wear:*** (Minimal Wear)

### Example 2 ###

  ***Name:*** Recoil Case


## /reloadcog ## 

**Description**

  Only used for debugging
