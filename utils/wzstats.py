import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import pandas as pd
import unidecode

# Xbox = xbox
# Battle.net = battle
# Playstation = psn

XBOX = 'xbl'
BNET = 'battle'
PSN = 'psn'

def getKD(user, platform):
    params = {
        'username': user,
        'platform': platform
    }

    r = requests.get('https://app.wzstats.gg/v2/player', params=params)

    return r.json()['data']['lifetime']['mode']['br']['properties']['kdRatio']

def getWins(user, platform):
    params = {
        'username': user,
        'platform': platform
    }

    r = requests.get('https://app.wzstats.gg/v2/player', params=params)

    j = r.json()

    return j['data']['lifetime']['mode']['br']['properties']['wins']

def getWinPct(user, platform):
    params = {
        'username': user,
        'platform': platform
    }

    r = requests.get('https://app.wzstats.gg/v2/player', params=params)

    j = r.json()

    return ((j['data']['lifetime']['mode']['br']['properties']['wins'] / j['data']['lifetime']['mode']['br']['properties']['gamesPlayed']) * 100)

def getKills(user, platform):
    params = {
        'username': user,
        'platform': platform
    }

    r = requests.get('https://app.wzstats.gg/v2/player', params=params)

    j = r.json()

    return j['data']['lifetime']['mode']['br']['properties']['kills']

def getKillsPerGame(user, platform):
    params = {
        'username': user,
        'platform': platform
    }

    r = requests.get('https://app.wzstats.gg/v2/player', params=params)

    j = r.json()

    return (j['data']['lifetime']['mode']['br']['properties']['kills'] / j['data']['lifetime']['mode']['br']['properties']['gamesPlayed'])

def getGulagLast100(user, platform):
    params = {
        'username': user,
        'platform': platform
    }

    r = requests.get('https://app.wzstats.gg/v2/player', params=params)

    j = r.json()

    return j['last100games']['gulagWinPercentage']

def getHSLast100(user, platform):
    params = {
        'username': user,
        'platform': platform
    }

    r = requests.get('https://app.wzstats.gg/v2/player', params=params)

    j = r.json()

    return (j['last100games']['headshots'] / j['last100games']['kills'])

def getKDLast100(user, platform):
    params = {
        'username': user,
        'platform': platform
    }

    r = requests.get('https://app.wzstats.gg/v2/player', params=params)

    j = r.json()

    return (j['last100games']['kills'] / j['last100games']['deaths'])

def getLast20Matches(user, platform):
    params = {
        'username': user,
        'platform': platform
    }

    r = requests.get('https://app.wzstats.gg/v2/player/match', params=params)

    j = r.json()
    
    matches = []

    for m in j:
        matches.append(m['id'])

    return matches

def getAvgKDMatch(match):
    params = {
        'matchId': match
    }

    r = requests.get('https://app.wzstats.gg/v2/', params=params)

    j = r.json()

    return j['matchStatData']['playerAverage']

def getMedianKDMatch(match):
    params = {
        'matchId': match
    }

    r = requests.get('https://app.wzstats.gg/v2/', params=params)

    j = r.json()

    return j['matchStatData']['playerMedian']

def getAvgTeamKDMatch(match):
    params = {
        'matchId': match
    }

    r = requests.get('https://app.wzstats.gg/v2/', params=params)

    j = r.json()

    return j['matchStatData']['teamAverage']

def getMedianTeamKDMatch(match):
    params = {
        'matchId': match
    }

    r = requests.get('https://app.wzstats.gg/v2/', params=params)

    j = r.json()

    return j['matchStatData']['teamMedian']

seen_accounts = []

def getLobbyStats(match, unique=False):
    params = {
        'matchId': match
    }
    try:
        r = requests.get('https://app.wzstats.gg/v2/', params=params)
        j = r.json()
    except:
        if unique:
            return [], []
        return []

   

    players = j['data']['players']

    unseen_players = []
    results = []

    for p in players:
        stat = p['playerStat']
        if stat != None:
            account = ""
            platform = ""

            if stat['battle'] != None or stat['psn'] != None or stat['xbl'] != None:
                if stat['battle'] != None:
                    account = stat['battle']
                    platform = 'battle'
                elif stat['psn'] != None:
                    account = stat['psn']
                    platform = 'psn'
                else:
                    account = stat['xbl']
                    platform = 'xbl'

                if unique and (not account in seen_accounts):
                    # seen_accounts.append(account)
                    unseen_players.append({'username': account, 'platform':platform})

            lifetime_kd = stat['lifetime']['mode']['br']['properties']['kdRatio']

            results.append({'id':match, 'username':account, 'platform':platform, 'lifetime_kd': lifetime_kd})

        else:
            print("Account not old enough/no decisive data.")
    if unique:
        return results, unseen_players

    return results

def loadAccounts(file_name, n):
    df = pd.read_csv(file_name)

    queue = []

    for index, account in df.iterrows():
        if not account["username"] in seen_accounts:
            queue.append(account)

    for i in range(n):
        print(i)
        next_user = queue.pop(0)
        while next_user["username"] in seen_accounts:
            next_user = queue.pop(0)
        seen_accounts.append(next_user['username']) 
        matches = getLast20Matches(next_user["username"], next_user["platform"])

        for match in matches:
            match_players, new_players = getLobbyStats(match, unique=True)
            # print(new_players)
            queue += new_players

            with open('./dataset/large.csv', 'a', newline='') as csvfile:   
                writer = csv.writer(csvfile, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)

                for match_player in match_players:
                    match_player['username'] = unidecode.unidecode(match_player['username'])
                    line = list(match_player.values())
                    writer.writerow(line)


loadAccounts("./config/accounts.csv", 125)