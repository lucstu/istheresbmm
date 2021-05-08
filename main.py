from csv import reader
from utils import wzstats as wz

tasks = []

with open('./config/accounts.csv', 'r') as read:
    f = reader(read)
    header = next(f)

    if header != None:
        for row in f:
            tasks.append((row[0], row[1]))

for t in tasks:
    matches = wz.getLast20Matches(t[0], t[1])
    
    # Compute data using functions from wzstats.py and write them to a new csv. We will then import that CSV to do analysis.

