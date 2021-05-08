import requests
from bs4 import BeautifulSoup

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

def getWinPct(user, platform):
    params = {
        'username': user,
        'platform': platform
    }

    r = requests.get('https://app.wzstats.gg/v2/player', params=params)

    j = r.json()

    return ((j['data']['lifetime']['mode']['br']['properties']['wins'] / j['data']['lifetime']['mode']['br']['properties']['gamesPlayed']) * 100)

def getKillsPerGame(user, platform):
    params = {
        'username': user,
        'platform': platform
    }

    r = requests.get('https://app.wzstats.gg/v2/player', params=params)

    j = r.json()

    return (j['data']['lifetime']['mode']['br']['properties']['kills'] / j['data']['lifetime']['mode']['br']['properties']['gamesPlayed'])

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
