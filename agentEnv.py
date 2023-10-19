import math
import matplotlib.pyplot as plt
from agents import Environment

class Rob_env(Environment):
    def __init__(self,walls = {}):
        """walls is a set of line segments 
               where each line segment is of the form ((x0,y0),(x1,y1))
        """
        self.walls = walls
        self.count = 0 #range of 10 movements for each wall in a direction and 10 in the opposite
        self.plots = [] 
    
    def mod_walls(self):
        for el in self.plots:
            for i in el:
                i.remove()
            plt.draw()
        self.plots = []
        new_walls = []
        for wall in self.walls:
            if wall[0][0] == wall[1][0]:
                m_wall = self.vert_mod(wall,self.count)
            elif wall[0][1] == wall[1][1]:
                m_wall = self.oriz_mod(wall,self.count)
            else:
                m_wall = self.diag_mod(wall,self.count)
            new_walls.append(m_wall)
            if self.count < 10 and self.count >=0:
                self.count += 1
            elif self.count == 10:
                self.count = -10
            else:
                self.count += 1
        
        self.walls = set(new_walls)
        return self.walls
    
    def vert_mod(self, wall, n):
        if n < 10 and n >= 0:
            new_wall = ((wall[0][0], wall[0][1]+1), (wall[1][0], wall[1][1]+1))
        elif n == 10:
            new_wall = ((wall[0][0], wall[0][1]+1), (wall[1][0], wall[1][1]+1))
        else:
            new_wall = ((wall[0][0], wall[0][1]-1), (wall[1][0], wall[1][1]-1))
        return new_wall

    def oriz_mod(self, wall, n):
        if n < 10 and n > 0:
            new_wall = ((wall[0][0]+1, wall[0][1]), (wall[1][0]+1, wall[1][1]))
        elif n == 10:
            new_wall = ((wall[0][0]+1, wall[0][1]), (wall[1][0]+1, wall[1][1]))
        else:
            new_wall = ((wall[0][0]-1, wall[0][1]), (wall[1][0]-1, wall[1][1]))
        return new_wall

    def diag_mod(self, wall, n):
        if n < 10 and n > 0:
            new_wall = ((wall[0][0]+1, wall[0][1]+1), (wall[1][0]+1, wall[1][1]+1))
        elif n == 10:
            new_wall = ((wall[0][0]+1, wall[0][1]+1), (wall[1][0]+1, wall[1][1]+1))
        else:
            new_wall = ((wall[0][0]-1, wall[0][1]-1), (wall[1][0]-1, wall[1][1]-1))
        return new_wall
    
        
import math
from agents import Environment
import matplotlib.pyplot as plt
import time

class Rob_body(Environment):
    def __init__(self, env, init_pos=(0,0,90)):
        """ env is the current environment
        init_pos is a triple of (x-position, y-position, direction) 
            direction is in degrees; 0 is to right, 90 is straight-up, etc
        """
        self.env = env
        self.rob_x, self.rob_y, self.rob_dir = init_pos
        self.turning_angle = 18   # degrees that a left makes
        self.whisker_length = 6   # length of the whisker
        self.whisker_angle = 30   # angle of whisker relative to robot
        self.crashed = False
        # The following control how it is plotted
        self.plotting = False      # whether the trace is being plotted
        self.sleep_time = 0.1     # time between actions (for real-time plotting)
        # The following are data structures maintained:
        self.history = [(self.rob_x, self.rob_y)] # history of (x,y) positions
        self.wall_history = []     # history of hitting the wall

    def percepts(self):
        return {'rob_x_pos':self.rob_x, 'rob_y_pos':self.rob_y,
                'rob_dir':self.rob_dir, 'whisker':self.whisker() , 'crashed':self.crashed}
    initial_percepts = percepts  # use percept function for initial percepts too

    def do(self,action):
        """ action is {'steer':direction}
        direction is 'left', 'right' or 'straight'
        """
        if self.crashed:
            return self.percepts()
        direction = action['steer']  
        compass_deriv = {'left':1,'straight':0,'right':-1}[direction]*self.turning_angle
        self.rob_dir = (self.rob_dir + compass_deriv +360)%360  # make in range [0,360)
        rob_x_new = self.rob_x + math.cos(self.rob_dir*math.pi/180)
        rob_y_new = self.rob_y + math.sin(self.rob_dir*math.pi/180)
        path = ((self.rob_x,self.rob_y),(rob_x_new,rob_y_new))
        if any(line_segments_intersect(path,wall) for wall in self.env.walls):
            self.crashed = True
            if self.plotting:
                plt.plot([self.rob_x],[self.rob_y],"r*",markersize=20.0)
                plt.draw()
        self.rob_x, self.rob_y = rob_x_new, rob_y_new 
        self.history.append((self.rob_x, self.rob_y))
        if self.plotting and not self.crashed:
            plt.plot([self.rob_x],[self.rob_y],"go")
            for wall in self.env.mod_walls():
                ((x0,y0),(x1,y1)) = wall
                lines = plt.plot([x0,x1],[y0,y1],"-k",linewidth=3)
                self.env.plots.append(lines)
            plt.draw()
            plt.pause(self.sleep_time)
        return self.percepts()

    def whisker(self):
        """returns true whenever the whisker sensor intersects with a wall
        """
        whisk_ang_world = (self.rob_dir-self.whisker_angle)*math.pi/180
            # angle in radians in world coordinates
        wx = self.rob_x + self.whisker_length * math.cos(whisk_ang_world)
        wy = self.rob_y + self.whisker_length * math.sin(whisk_ang_world)
        whisker_line = ((self.rob_x,self.rob_y),(wx,wy))
        hit = any(line_segments_intersect(whisker_line,wall)
                    for wall in self.env.walls)
        if hit:
            self.wall_history.append((self.rob_x, self.rob_y))
            if self.plotting:
                plt.plot([self.rob_x],[self.rob_y],"ro")
                plt.draw()
        return hit


def line_segments_intersect(linea,lineb):
    """returns true if the line segments, linea and lineb intersect.
    A line segment is represented as a pair of points.
    A point is represented as a (x,y) pair.
    """
    ((x0a,y0a),(x1a,y1a)) = linea
    ((x0b, y0b), (x1b, y1b)) = lineb
    da, db = x1a-x0a, x1b-x0b   #da = distance between previous robot x position and new one 
                                #db = distance between first point wall and second one (x axis)
    ea, eb = y1a-y0a, y1b-y0b   #ea = distance between previous robot y position and new one
                                #eb = distance between first point wall and second one (y axis)
    denom = db*ea-eb*da
    if denom==0:    # line segments are parallel
        return False
    cb = (da*(y0b-y0a)-ea*(x0b-x0a))/denom  # position along line b
    if cb<0 or cb>1:
        return False
    ca = (db*(y0b-y0a)-eb*(x0b-x0a))/denom # position along line a
    return 0<=ca<=1
      
# Test cases:
# assert line_segments_intersect(((0,0),(1,1)),((1,0),(0,1)))
# assert not line_segments_intersect(((0,0),(1,1)),((1,0),(0.6,0.4)))
# assert line_segments_intersect(((0,0),(1,1)),((1,0),(0.4,0.6)))