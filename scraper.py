from bs4 import BeautifulSoup
import requests
import json

BASE_URL  = "http://www.foxsports.com"
TABLE_URL = "/mlb/players?season=2016&page=%d&position=0"
players = []

def run():
    # start on page 26
    for x in range(26, 56):
        r = requests.get(BASE_URL + TABLE_URL % x)
        soup = BeautifulSoup(r.text, 'html.parser')
        player_table = soup.find('table', class_='wisfb_standard')
        scrape_table(player_table)
        with open('db.json', 'w') as f:
            json.dump(players, f)

def scrape_table(player_table):
    player_rows  = player_table.find_all('tr')
    for player_row in player_rows:
        player_link = player_row.find('a')
        if player_link != None:
            # follow link and add image_url
            r = requests.get(BASE_URL + player_link.get('href'))
            player_page = BeautifulSoup(r.text, 'html.parser')
            scrape_player(player_page)
            
def scrape_player(player_page):
    player = player_page.find('img', class_='wisfb_headshotImage wisfb_bioLargeImg')
    if player != None:
        player_image = player.get('src')
        if player_image != '#':
            global players
            # create json object with player
            player = {'image_url':player_image, 'name':player.get('alt')}
            players.append(player)
            print(str(len(players)) + " " + str(player))

run()
print ("Done! All " + str(len(players)) + " players have been added")