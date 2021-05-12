import utils.wzstats as wz
import csv
import pandas as pd

df = pd.read_csv('./dataset/users.csv')

for index, x in df.iterrows():
    game_ids = x.gameIDs.split(';')
    with open('./dataset/games.csv', 'a', newline='') as csvfile:   
        writer = csv.writer(csvfile, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
        
        for id in game_ids:
            lobby = wz.getLobbyStats(str(id))
            for player in lobby:
                player['DMG'] = player['DMG'].replace(',', '')
                line = list(player.values())
                writer.writerow(line)