from bs4 import BeautifulSoup
import requests
import json

BASE_URL  = "http://www.foxsports.com"
TABLE_URL = "/mlb/players?season=2016&page=%d&position=0"
PAGE_COUNT = 56
players = []

def run():
    for x in range(1, PAGE_COUNT+1):
        r = requests.get(BASE_URL + TABLE_URL % x)
        soup = BeautifulSoup(r.text, 'html.parser')
        player_table = soup.find('table', class_='wisfb_standard')
        scrape_table(player_table)
        with open('db4.json', 'a') as f:
            s = ""
            if x == 0:
                s = json.dumps(players).replace(']', ',')
            elif x == PAGE_COUNT:
                s = json.dumps(players).replace('[', '')
            else:
                s = json.dumps(players).replace('[', '').replace(']', ',')
            f.write(s)
            print "Appended page " + str(x)

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