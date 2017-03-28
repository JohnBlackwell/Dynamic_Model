# @author: sheriff@live.unc.edu

# Portions of this code borrowed from roos@cs.umd.edu's implementation of the axelrod agent-based model 2014

# Main class for Dynamic Social Identity Model


#### modules for the GUI ########
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import ListedColormap
import pycxsimulator
import numpy as np

##### modules for agent module ###
import random as rnd
import agent as agent
from matrix import *

#####Agent Attributes

# Order   Attribute
#
# 1        Gender: Male or Female
# 2        Age: int 0-100
# 3        Attractive: Yes or No
# 4        Race: Black, White, Asian, Hispanic
# 5        Hair color: Brown, Black, Asian, Red, Blonde
# 6        Eye color: Blue, Brown, Green


Gender = ['male', 'female']
Age = range(0, 80)
Attractive = ['YES', 'NO']
Race = ['Black', 'White', 'Asian', 'Hispanic']
Hair_Color = ['Brown', 'Black', 'Red', 'Blonde']
Eye_Color = ['Blue', 'Brown', 'Green']

GUI = False  # we are using a GUI

########## Setting Up Main Environment Params #############
nTags = 2
tags = range(1, nTags + 1)  # list of tags (1,2,..., nTags-1)
nPlayers = 200  # number of players

PS = [(-3, 0),  # agents will interact with others in this personal space of x, y offsets
      (0, -3),
      (0, +3),
      (+3, 0)]

maxtime = 50  # length of simulation if we aren't using the GUI

m = 30  # temp value for rows
n = 30  # temp value for col

agentGroup = []  # array storing agents creating at population round


def init():
    global time, grid, agentGroup
    time = 0
    grid = Matrix(m, n, PS)

    # need to also initialize GUI set up here
    registerCmap(nTags)  # for visualization


def populate():  # this populates the grid
    global agentGroup, grid

    emptySites = grid.get_empty_sites()
    #print(emptySites)
    randEmptySitesToPopulate = rnd.sample(emptySites, nPlayers)
    # print(randEmptySitesToPopulate)


    # populate the randomly chosen empty sites
    for loc in randEmptySitesToPopulate:
        participant = createAgent()
        #set initial Male/Female

        if participant.getOrder(1) == "male":
            participant.tag = 1
        else:
            participant.tag = 2

        grid.place_agent(participant, loc[0], loc[1])

        agentGroup.append(participant)

    # for person in agentGroup:
    #     print(person.getOrder(1) + " ", person.tag)



def imp_model():
    global time, grid, agentGroup

    # returns a list of pairs (agent, neighbor)
    total_neighbors_list = grid.get_neighbors()
    # this list is for an individual agent
    agent_list = list()

    # the following code is conditional on the agents HAVING NEIGHBORS
        ###### LEFT OFF HERE 02/24
    if len(total_neighbors_list) > 0:
        #choose an agent from each tuple and put it in a list
        #every round, iterate through this list in order to get more movement
        for each_tuple in total_neighbors_list:
            # choose either the agent or its neighbor
            an_agent = each_tuple[rnd.randint(0, 1)]
            agent_list.append(an_agent)

        agent_neighbors_list = getNeighbors(agent_list, total_neighbors_list)

        print(agent_neighbors_list)
        woman_count_dict = {'woman_count': None, 'grid_loc': None}
        for each_ag in agent_neighbors_list:
            if len(agent_neighbors_list) > 1:
                if getMaleNeighbors(agent_neighbors_list) >= (len(agent_neighbors_list) // 2) + 1:
                    for ag in agentGroup:
                        ag_neigh_list = getNeighbors(agentGroup, total_neighbors_list)
                        womanNeighCount(ag_neigh_list, woman_count_dict)



            # iterate through list to find order matches


    else:
        time += 1


def draw():
    """Draws the agent grid for visualization."""

    # clear plt and arrange suplots
    plt.cla()
    gs = gridspec.GridSpec(3, 2, width_ratios=[2, 1], height_ratios=[0.25, 1, 0.25])
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=None)
    cmap = matplotlib.cm.get_cmap()

    # get tag matrix to plot in main plot
    tagMatrix = np.zeros([m, n])  # matrix with each entry being the agent tag at that spot in grid
    setTagMatrix(agentGroup, tagMatrix)
    #  # print tagMatrix

    ################################### Main Tag Color Plot
    ax = plt.subplot(gs[:, 0])
    #ax.patch.set_facecolor('gray')
    ax.grid(False)
    ax.set_aspect('equal')

    # #plot tag colors
    plt.pcolor(tagMatrix, edgecolors='k', linewidths=0, cmap=cmap)
    # plt.axis([0,n,0,n])
    #ax.imshow(tagMatrix, cmap=cmap, vmin=0, vmax=nTags + 1, interpolation='nearest')

    # plot time
    ax.text(26.5, 1, "Time " + str(time))


#### HELPER FUNCTIONS #####


def createAgent():
    """" Create Agent with random attributes"""
    return agent.Agent(rnd.choice(tags), rnd.choice(Gender), rnd.randint(10, 80), rnd.choice(Attractive),
                       rnd.choice(Race), rnd.choice(Hair_Color), rnd.choice(Eye_Color))

def getNeighbors(agent_list, total_neighbors_list):

    agent_neighbors_list = list()
    for an_agent in agent_list:
        for neigh in total_neighbors_list:
            for select_agent in neigh:
                if select_agent.gridlocation == an_agent.gridlocation and select_agent.gridlocation == neigh[0].gridlocation:
                    agent_neighbors_list.append(neigh[1])
                elif select_agent.gridlocation == an_agent.gridlocation and select_agent.gridlocation == neigh[1].gridlocation:
                    agent_neighbors_list.append(neigh[0])
                else:
                    continue
    return agent_neighbors_list

def getMaleNeighbors(agent_neighbors_list):

    male_count = 0
    for ag in agent_neighbors_list:
        if ag.getOrder(1) == 'Male':
            male_count += 1
    return male_count

def womanNeighCount(ag_neigh_list, woman_count_dict):

    woman_count = 0
    for ag in ag_neigh_list:
        if ag.getOrder(1) == 'Woman':
            woman_count += 1
    woman_count_dict['woman_count', 'grid_loc'] = woman_count, ag.gridlocation
    return woman_count




def setTagMatrix(agentGroup, M):
    """ Set the matrix M so that each entry is the tag identifier for the agent at that location. """
    for each_agent in agentGroup:
        (x, y) = each_agent.gridlocation
        M[x, y] = each_agent.tag


def registerCmap(nTags):
    """ Create a colormap with N (N<=15) discrete colors and register it. """
    # define individual colors as hex values

    cpool = ['#ffffff', '#7EA7D8', '#F7977A', '#FFF79A', '#A2D39C',
             '#FF00FF', '#FFFF00', '#ea2ec4', '#ea2e40', '#cdcdcd',
             '#577a4d', '#2e46c0', '#f59422', '#219774', '#8086d9']
    mycmap = matplotlib.colors.ListedColormap(cpool[0:nTags + 1], 'index')
    matplotlib.cm.register_cmap(cmap=mycmap)


def main():
    global time

    init()
    populate()

    while time < maxtime:
        imp_model()
        #leave draw commented out because draw() still needs work
        # draw()


# run simulation either with or without GUI
if GUI:

    #go to the pycxsimulator code and find start func
    #the four args below are passed into pycxsimulator which uses Tkinter to make the GUI
    pycxsimulator.GUI().start(func=[init, populate, draw, imp_model])
else:

    #it is advised to add print statements throughout the model in order to track agent movements if running
    #main without a GUI
    main()
