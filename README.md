# lolWikiScraping

## Intro
simple python script to get the aram changes for every champion

This script scrap the [leagueoflegends wiki](https://leagueoflegends.fandom.com/wiki/Module:ChampionData/data) page to get the information of every champ including the changes for each game mode.

Tu use it just run $ python3 AramChangesFinder.py CHAMP GAME_MODE
* **CHAMP:** the champ to search
* **GAME_MODE:** the stats of the game mode to return, if no game mode is specified it will use aram as default

## Example
![Example](Images\Use_example.png)

## Dependencies

* pip install requests   
* pip install beautifulsoup4