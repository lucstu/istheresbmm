from csv import writer, reader
from utils import wzstats as wz
import pandas as pd

tasks = []

with open('./config/accounts.csv', 'r') as read:
    f = reader(read)
    header = next(f)

    if header != None:
        for row in f:
            tasks.append((row[0], row[1]))

for t in tasks:
    name = t[0]
    plat = t[1]
    kd = wz.getKD(name, plat)
    winpct = wz.getWinPct(name, plat)
    wins = wz.getWins(name, plat)
    kills = wz.getKills(name, plat)
    killsPerGame = wz.getKillsPerGame(name, plat)
    gulagLast100 = wz.getGulagLast100(name, plat)
    hsLast100 = wz.getHSLast100(name, plat)
    kdLast100 = wz.getKDLast100(name, plat)
    gameIDs = wz.getLast20Matches(name, plat)
    gameIDs = ";".join(gameIDs)

    result = [name, plat, kd, winpct, wins, kills, killsPerGame, gulagLast100, hsLast100, kdLast100, gameIDs]

    with open('./dataset/users.csv', 'a', newline='') as f:
        _writer = writer(f)
        _writer.writerow(result)
        f.close()

df = pd.read_csv('./dataset/users.csv')
df['game']