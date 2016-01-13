from bs4 import BeautifulSoup
import requests
import json

BASE_URL = "http://mlb.mlb.com"
players = []

def run():
    r = requests.get(BASE_URL + '/dr/active_players.jsp')
    soup = BeautifulSoup(r.text, 'html.parser')
    page_nums = soup.find(class_="page_nums")
    page_links = [link.get('href') for link in page_nums.find_all('a')]
    pages = [requests.get(BASE_URL + page_link) for page_link in page_links]
    #[scrape_table(table_page.text) for table_page in pages]
    scrape_table(pages[0].text)
    with open('db.json', 'w') as f:
        json.dump(players, f)
    

def scrape_table(table_page):
    soup = BeautifulSoup(table_page, 'html.parser')
    players_table = soup.find(class_='players_table')
    # put all players from table into list
    players_links = [player_link.get('href') for player_link in players_table.find_all('a')]
    players_pages = [requests.get(BASE_URL + player_link) for player_link in players_links]
    [scrape_player(player_page.text) for player_page in players_pages]

def scrape_player(player_page):
    soup = BeautifulSoup(player_page, 'html.parser')
    player = soup.find('img', class_='player-headshot')
    if player != None:
        global players
        # create json object with player
        player = {'image_url':player.get('src'), 'name':player.get('alt')}
        players.append(player)
        print(str(len(players)) + " " + str(player))

run()
print ("Done! All " + str(len(players)) + " players have been added")