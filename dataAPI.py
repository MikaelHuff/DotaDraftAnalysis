import requests
import numpy as np

# This file is used to pull the data from the API and store it as numpy array files
# NOTE: I removed the API key so this will not work as free calls are limited per minute

# Pull all the heroes in the game from OpenDota API, then saves their name in a matrix that gets saved to file
api_key = "api_key=55ee8d04-6477-41ad-acf0-0758be4f75dd"
heroIDPull = requests.get("https://api.opendota.com/api/heroes?"+api_key)
heroAm = len(heroIDPull.json())
heroIDs = np.empty([heroAm],dtype=np.dtype('U100'))
for hero in range(heroAm):
    heroIDs[hero] = heroIDPull.json()[hero]["name"][14:]

np.save('dataID', heroIDs)

# Pulls matchups data from API, for each matchup pair, we have hero and their opponent, games played, and games won
# Saves to file the array of the data, as well as a vector including all the hero ID numbers that are unused in game.
skips = 1
skips2 = 0
vsArr = np.zeros([heroAm, heroAm, 3])

hero = 0
emptyIDs = -1*np.ones(20)
while hero < heroAm:
    print(hero)
    url = "https://api.opendota.com/api/heroes/"+str(hero+skips)+"/matchups?" + api_key
    response = requests.get(url)
    if len(response.text) <= 10:
        emptyIDs[skips-1] = hero+skips
        print('skipping '+str(hero+skips))
        skips = skips + 1
        continue
    skips2 = 0
    for counter in range(len(response.json())):
        if hero == counter:
            vsArr[hero][counter+skips2][0] = hero+skips
            skips2 = 1
        vsArr[hero][counter+skips2][0] = response.json()[counter]["hero_id"]
        vsArr[hero][counter+skips2][1] = response.json()[counter]["games_played"]
        vsArr[hero][counter+skips2][2] = response.json()[counter]["wins"]
    hero = hero + 1
np.save('dataVS', vsArr)
np.save('emptyIDs', emptyIDs)

