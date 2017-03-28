# @author: sheriff@live.unc.edu

# Portions of this code borrowed from Agent class created by @roos.umd.edu for the Axelrod agent-based model 2014

# Agent class for Dynamic Social Identity Model


class Agent:
    def __init__(self, Gender, Age, Attractive, Race, Hair_Color, Eye_Color, gridLoc=None, tag = None):


        #In future updates to this code, tag will be used to identity this agent and link to its attributes
        #possibly use tag as a key to attribute dict
        #for now, tag is merely linked to a color to differentiate agents in the GUI
        self.tag = tag

        #the five attributes associated with each agent
        self.Gender = Gender
        self.Age = Age
        self.Attractive = Attractive
        self.Race = Race
        self.Hair_Color = Hair_Color
        self.Eye_Color = Eye_Color

        #(x,y) tuple
        self.gridlocation = gridLoc

        # ordered list containing attributes
        self.ordergroup = [Gender, Age, Attractive, Race, Hair_Color, Eye_Color]

    def getOrder(self, order):
        # print(order)
        # print(self.ordergroup[order])
        return self.ordergroup[order]
