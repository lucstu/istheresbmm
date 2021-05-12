import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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

def getLobbyStats(match):
    # driver = webdriver.Chrome('./chromedriver.exe')
    driver = webdriver.Chrome('/Users/sandeep/Workspace/chromedriver')
    driver.get('https://wzstats.gg/match/' + match)
    time.sleep(10)
    source = driver.page_source
    driver.close()

    soup = BeautifulSoup(source, 'html.parser')
    entries = soup.find_all('div', {'class':'team-container'})

    total = []

    for e in entries:
        container = e.find('div', {'class':'team-players-info-container table-cell'})
        players = container.find_all('div', {'class':'team-players-info-table'})[1:]
        for p in players:
            stats = p.find_all('div', {'class':'team-players-info-cell'})
            kills = stats[0].find('div', {'class':'stat-value'}).text.strip()
            kd = stats[1].find('div', {'class':'stat-value'}).text.strip()
            dmg = stats[2].find('div', {'class':'stat-value'}).text.strip()
            deaths = stats[3].text.strip()
            headshot = stats[4].text.strip()
            result = {'ID': match, 'Kills': kills, 'KD': kd, 'DMG': dmg, 'Deaths': deaths, 'Headshot': headshot}
            total.append(result)

    return total
