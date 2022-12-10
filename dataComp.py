import numpy as np

# This file is used to rearrange the data pulled from the API into a more easily usable form.


class data:
    # Two of these variables, heroAm and vsArr, are used only within this class.
    # The rest are 3 things that can be called later by other functions
    # self.heroNames is a list of all Heroes Names, sorted by their ID number

    def __init__(self):
        self.heroNames = np.ndarray.tolist(np.load('dataID.npy'))
        self.heroAm = len(self.heroNames)
        self.vsArr = self.fixEmpty(np.load('dataVS.npy'))
        self.heroStats = self.sortStats()
        self.weights = self.findWeights()

    def getStats(self):
        return self.heroStats

    def getHeroList(self):
        return self.heroNames

    def getWeights(self):
        return self.weights

    # Takes the data and turns it into more suitable array for use
    # Array is of shape: heroAM x heroAM x 3 where heroAM is amount of heroes
    # First index is for each hero, second index is for each hero as the opponent,
    # # and the final index represents heroID, games in this matchup, wins to hero of first index
    # for each hero, ie vsArr[i,:,:] for each i, we sort by their matchups by the hero ID and then
    # remove the value for ID, as we can now just deal with the index
    def sortStats(self):
        vsArrSort = np.empty([self.heroAm,self.heroAm,2])

        for hero in range(self.heroAm):
            order = np.argsort(self.vsArr[hero,:,0])
            for opponent in range(self.heroAm):
                if hero == opponent:
                    continue
                vsArrSort[hero, opponent] = self.vsArr[hero, order[opponent], 1:]
            vsArrSort[hero,hero] =[np.sum(vsArrSort[hero,:,0]), np.sum(vsArrSort[hero,:,1])]
        vsArrSort[:,:,1] = vsArrSort[:,:,1]/vsArrSort[:,:,0]
        return vsArrSort

    # As some heroes may not have any matches against certain other heroes
    # (due to API not giving lifetime data, but data from only current development
    # version of the game), this function will figure out which IDs are missing and
    # put the ID in with 2 games total and 1 game won.
    # This is needed as otherwise the above function sortStats sorting would not work properly
    def fixEmpty(self, vsArr):
        emptyIDs = np.load('emptyIDs.npy')
        for i in range(self.heroAm):
            id = 1
            for j in range(self.heroAm):
                k = 0
                while vsArr[i,j,0] == 0:
                    if (id not in vsArr[i,:,0]) and (id not in emptyIDs):
                        vsArr[i, j, 0] = id
                        vsArr[i,i,1] = 2
                        vsArr[i,i,1] = 1
                    id = id + 1

        return vsArr

    # Assumes that the data is distributed normally. Here, we are assuming 3 pulls from a distribution
    # 1. A heroes total amount of games versus the average games for a hero
    # 2. A heroes amount of games with an opponent versus the average amount of games for an opponent
    # 3. The matchups winrate versus the heroes total winrate.
    # After calculating the parameters for these distributions, we then derive a weight for each matchup.
    # This weight is a sigmoid where the x value is the number of standard deviations from the mean.
    def findWeights(self):
        matchAmParameters = np.zeros([self.heroAm, 2])
        winrateParameters = np.zeros([self.heroAm, 2])

        matchAmParameters[:, 0] = np.diagonal(self.heroStats[:, :, 0])/(self.heroAm-1)
        winrateParameters[:, 0] = np.diagonal(self.heroStats[:, :, 1])
        expectedTotalGames = np.sum(np.diagonal(self.heroStats[:,:,0]))/(10*self.heroAm)
        varTotalGames = 0

        for m in range(self.heroAm):
            varTotalGames = varTotalGames + (self.heroStats[m,m,0]-expectedTotalGames)**2
            for n in range(self.heroAm):
                if m != n:
                    matchAmParameters[m, 1] = matchAmParameters[m, 1] + (self.heroStats[m,n,0]-matchAmParameters[m,0]) ** 2
                    winrateParameters[m, 1] = winrateParameters[m, 1] + (self.heroStats[m,n,1]-winrateParameters[m,0]) ** 2

        matchAmParameters[:,1] = matchAmParameters[:,1]/(self.heroAm-2)
        winrateParameters[:,1] = winrateParameters[:,1]/(self.heroAm-2)
        varTotalGames = varTotalGames/self.heroAm

        matchAmWeights = np.zeros([self.heroAm,self.heroAm])
        winrateWeights = np.zeros([self.heroAm,self.heroAm])
        weightMultiplier = 10
        for m in range(self.heroAm):
            for n in range(self.heroAm):
                if m == n:
                    matchAmWeights[m,n] = 1/(1+np.exp((100*weightMultiplier)*(self.heroStats[m,n,0]-expectedTotalGames)/varTotalGames))
                    continue
                matchAmWeights[m, n] = 1 / (1 + np.exp(weightMultiplier*(self.heroStats[m, n, 0] - matchAmParameters[m,0]) / matchAmParameters[m,1]))
                winrateWeights[m, n] = 1 / (1 + np.exp((.04*weightMultiplier)*(self.heroStats[m, n, 1] - winrateParameters[m,0]) / winrateParameters[m,1]))

        matchAmWeights = np.nan_to_num(matchAmWeights)
        winrateWeights = np.nan_to_num(winrateWeights)

        return [matchAmWeights, winrateWeights]







dat = data()