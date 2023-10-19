from agentMiddle import Rob_middle_layer
from agents import Environment
from math import sqrt as sr

class Rob_top_layer(Environment):
    def __init__(self, middle, timeout=200, locations = { 
                'o111': (80, 0), 'o103':(20,20), 'o104':(40,10), 'o109':(50,50),'storage':(101,51)}):
        """middle is the middle layer
        timeout is the number of steps the middle layer goes before giving up
        locations is a loc:pos dictionary 
            where loc is a named location, and pos is an (x,y) position.
        """
        self.middle = middle
        self.timeout = timeout  # number of steps before the middle layer should give up
        self.locations = locations

    
    def do(self,plan):
        """carry out actions.
        actions is of the form {'visit':list_of_locations}
        It visits the locations in turn.
        """
        to_do = plan['visit']
        x0 = 0 
        y0 = 0   
        new_to_do = {}
        for loc in to_do:
            x1 = self.locations[loc][0]
            y1 = self.locations[loc][1]
            distance = sr(pow((x1-x0), 2) + pow((y1-y0), 2))
            new_to_do.update({loc:distance})
        new_to_do = sorted(new_to_do.items(), key=lambda x:x[1])
        to_do = []
        for i in range(0, len(new_to_do)):
            to_do.append(new_to_do[i][0])
        for loc in to_do:
            position = self.locations[loc]
            arrived = self.middle.do({'go_to':position, 'timeout':self.timeout}) #richiama funzione do di agentMiddle
            self.display(1,"Arrived at",loc,arrived)


import matplotlib.pyplot as plt

class Plot_env(object):
    def __init__(self, body,top):
        """sets up the plot
        """
        self.body = body
        plt.ion()
        plt.clf()
        plt.axes().set_aspect('equal')
        for wall in body.env.walls:
            ((x0,y0),(x1,y1)) = wall
            lines = plt.plot([x0,x1],[y0,y1],"-k",linewidth=3)
            body.env.plots.append(lines)
        for loc in top.locations:
            (x,y) = top.locations[loc]
            plt.plot([x],[y],"k<")
            plt.text(x+1.0,y+0.5,loc) # print the label above and to the right
        plt.plot([body.rob_x],[body.rob_y],"go")
        plt.draw()        

    def plot_run(self):
        """plots the history after the agent has finished.
        This is typically only used if body.plotting==False
        """
        xs,ys = zip(*self.body.history)
        plt.plot(xs,ys,"go")
        wxs,wys = zip(*self.body.wall_history)
        plt.plot(wxs,wys,"ro")
        plt.draw()

from agentEnv import Rob_body, Rob_env
import numpy as np

env = Rob_env(
    {
    (
        (20, 0), (30, 20)
    ),
    (
        (70, -5), (70, 25)
    )
    }) #walls 
body = Rob_body(env) #Rob_body costruttore 
body.plotting = True
middle = Rob_middle_layer(body) #Rob_middle_layer costruttore 
top = Rob_top_layer(middle) #Rob_top_layer costruttore 

# try:
pl=Plot_env(body,top)
top.do({'visit':['o109','storage','o104','o103']})
pl.plot_run()
# You can directly control the middle layer:
#middle.do({'go_to':(30,-10), 'timeout':200})
# Can you make it crash?

# Robot Trap for which the current controller cannot escape:
""" trap_env = Rob_env({((10,-21),(10,0)), ((10,10),(10,31)), ((30,-10),(30,0)),
                    ((30,10),(30,20)),  ((50,-21),(50,31)), ((10,-21),(50,-21)),
                    ((10,0),(30,0)),  ((10,10),(30,10)),  ((10,31),(50,31))})
trap_body = Rob_body(trap_env,init_pos=(-1,0,90))
trap_middle = Rob_middle_layer(trap_body)
trap_top = Rob_top_layer(trap_middle,locations={'goal':(71,0)}) """

# Robot trap exercise:
# pl=Plot_env(trap_body,trap_top)
# trap_top.do({'visit':['goal']})

