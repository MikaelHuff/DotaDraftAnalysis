import numpy as np
import dataComp

# This file takes a set of 10 heroes (with teams defined) and returns an array representing
# each of the 5x5=25 matchups per team, then the margin of the array, aka the rating of each hero
# and finally the total rating to decide which team has the advantage.
data = dataComp.data()

# This function just chooses a random draft of 10 heroes while ensuring that there is
# no duplicates amongst them.
def randomise(heroAm):
    nums = -1*np.ones(10)
    nums[0] = np.random.randint(0, heroAm)
    for i in range(10-1):
        new = 1
        while new == 1:
            new = 0
            nums[i+1] = np.random.randint(0, heroAm)
            for j in range(i+1):
                if nums[j] == nums[i+1]:
                    new = 1
    return nums.astype(int)

# As said in the file comment, returns a 6x6 array containing all the important values
# The second input paramater works as a boolean to decide if the weights found in dataComp.py
# should be used over the raw winrate values.
def findRatings(draft, calctype):
    draftIDs = -1*np.ones(10)
    heroIDs = data.getHeroList()
    results = np.zeros([6,6])
    weights = data.getWeights()
    winrates = data.getStats()[:,:,1]-.5
    for i in range(10):
        draftIDs[i] = heroIDs.index(draft[i])

    for hero in range(10):
        for opponent in range(5):
            hero1ID = int(draftIDs[hero])
            hero2ID = int(draftIDs[2*opponent+(hero+1)%2])
            matchupRating = winrates[hero1ID, hero2ID]
            if calctype == 'weighted':
                matchupRating = matchupRating * (weights[0][hero1ID][hero2ID]*weights[1][hero1ID][hero2ID])
            if hero%2 == 0:
                results[int(hero/2), opponent] = results[int(hero/2), opponent] + matchupRating
                results[int(hero/2),5] = results[int(hero/2),5] + matchupRating * weights[0][hero1ID][hero1ID]
            if hero%2 == 1:
                results[opponent, int(hero/2)] = results[opponent, int(hero/2)] + (-1)*matchupRating
                results[5,int(hero/2)] = results[5,int(hero/2)] + (-1)*matchupRating * weights[0][hero1ID][hero1ID]

    results[5,5] = np.sum(results[:,5])+np.sum(results[5,:])
    return results




values = {'_A1_': 'drow_ranger', '_B1_': 'troll_warlord', '_A2_': 'primal_beast', '_B2_': 'nyx_assassin', '_A3_':
        'naga_siren', '_B3_': 'meepo', '_A4_': 'gyrocopter', '_B4_': 'skywrath_mage', '_A5_': 'huskar', '_B5_': 'spectre'}
draft = list(values.values())
findRatings(draft,'raw winrate')





