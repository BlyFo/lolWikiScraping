# lolWikiScraping

## Intro
simple python script to get the aram changes for every champion

This script scrap the [leagueoflegends wiki](https://leagueoflegends.fandom.com/wiki/Module:ChampionData/data) page to get the information of every champ including the changes for each game mode.

Tu use it just run $ python3 AramChangesFinder.py CHAMP GAME_MODE
* **CHAMP:** the champ to search
* **GAME_MODE:** the stats of the game mode to return, if no game mode is specified it will use aram as default

## Example
![Example](https://github.com/BlyFo/lolWikiScraping/blob/main/Images/Use_example.png)   
**(For anivia in parch 13.24)**   

## Dependencies

* pip install requests   
* pip install beautifulsoup4
