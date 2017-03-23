

# Matrix class for creating m x n grid
# author: sheriff@live.unc.edu
# Portions of this code borrowed from Torus class created by @roos.umd.edu for the Axelrod agent-based model 2014
#
#



class Matrix:


    def __init__(self, ncols, nrows, PS):


        self.ncols = ncols
        self.nrows = nrows
        #PS being the bounds in which agent will interact with neighbors. Set in main class
        self.PS = PS
        self.agentMatrix = [[None] * ncols for i in
                            range(nrows)]  # ncols x nrows matrix that has agent or None at each location

        self.emptySites = [(i, j) for i in range(nrows) for j in range(ncols)]
        self.neighborLocs = {}  # for each location (x,y) key will hold neighboring locations as list

        #these nested for loops return a list that contains all of the neighbors at a particular (x,y) coordinate
        for i in range(self.nrows):
            for j in range(self.ncols):
                neighLocs = list()
                for offset in self.PS:
                    dc, dr = offset  # note: x,y neighborhood
                    r = (i + dr) % nrows
                    c = (j + dc) % ncols
                    neighLocs.append((r, c))
                self.neighborLocs[(i, j)] = neighLocs

    def place_agent(self, agent, x, y):
        """
        Places agent on grid at (x,y).
        """

        agent.gridlocation = (x, y)
        self.agentMatrix[x][y] = agent
        self.emptySites.remove((x, y))


    def move_agent(self, agent, x, y):
        """ Moves agent to loc. """
        self.agentMatrix[agent.gridlocation[0]][agent.gridlocation[1]] = None
        self.emptySites.append(agent.gridlocation)
        self.agentMatrix[x][y] = agent
        self.emptySites.remove(agent.gridlocation)
        agent.gridlocation = (x,y)

    def get_empty_sites(self):
        """
        Returns list of (x,y) tuples that are empty grid locations.
        """

        return self.emptySites

    def get_neighbors(self):
        """
        Return neighbors of agent.
        """

        pairs = set()
        for origLoc in self.neighborLocs.keys():
            if self.agentMatrix[origLoc[0]][origLoc[1]] is not None:  # there is an agent here
                for loc in self.neighborLocs[origLoc]:

                    if self.agentMatrix[loc[0]][loc[1]] is not None:  # there is an agent at this neighboring loc
                        pairs.add((self.agentMatrix[origLoc[0]][origLoc[1]], self.agentMatrix[loc[0]][loc[1]]))

        return list(pairs)






