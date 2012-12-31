from Tkinter import *

# ----------------------
# Space Station Lockout
# In this problem you are to build a planner that finds a solution for a
# Space Station Lockout game.
#
# In this problem, a game is represented by an array indicating the position
# of the carbon based unit and its bot helpers:
#
#  [[1,1], [0, 1], [0, 2], [3, 3], [4,1]]
#   
#  The first element of the array indicates the carbon-based unit and the other
#  elements are the bot helpers. This array represents the following position
#  where X represents the carbon-based unit, 1-4 are the bot helpers and the O
#  indicates the airlock:
#                             [[3,3], [0,0], [0, 2], [1, 4], [2, 0], [4, 1]]
#   +---+---+---+---+---+     +---+---+---+---+---+   
#   |   | 1 | 2 |   |   |     | 1 |   | 4 |   |   |
#   +---+---+---+---+---+     +---+---+---+---+---+
#   |   | X |   |   |   |     |   |   |   |   | 5 |
#   +---+---+---+---+---+     +---+---+---+---+---+
#   |   |   | O |   |   |     | 2 |   | O |   |   |
#   +---+---+---+---+---+     +---+---+---+---+---+
#   |   |   |   | 3 |   |     |   |   |   | X |   |
#   +---+---+---+---+---+     +---+---+---+---+---+
#   |   | 4 |   |   |   |     |   | 3 |   |   |   |
#   +---+---+---+---+---+     +---+---+---+---+---+
#
#  The playing board is 5 x 5 squares. The idea is that you on the outside of
#  a  space station with your bots; an emergency occurred and you must reach
#  the escape hatch (the center square) to return to the safety of the station.
#  A piece can move up, down, left, or right. A piece can only stop by being
#  blocked by another piece. If it is not blocked it flies off the edge of the
#  board. If the piece is stopped at the airlock, it is removed from the board.
#  Again, the goal of the game is for the carbon unit to reach the airlock.
#
#  A solution to the problem is given as a list of moves. For example, a solution
#  to the above problem is
#
#   [[0, 'South'], [0, 'East'], [0, 'North'], [1, 'South'], [3, 'West'], [0, 'South']]
#
#  meaning the carbon-based unit goes South and then East, and North.Then Unit 1 moves
#  South, and so on.
#  
#  -----------------------------------
#
#  Programmer Instructions:
#
#  This is to be done individually without outside help.
#
#  Write the method getSolution which starts on line 170. The function should return a
#  list of moves.  (180XP)
#
#  A PriorityQueue class is provided for you
#  The getSuccessors method returns a list of successor states to a particular
#  game state
#
#  Optional (worth 70XP): write a method checkSolution that takes a game and a solution
#  as arguments and returns True if the solution is indeed a solution to the game
#  and False otherwise

import heapq
import copy
class PriorityQueue:
  """
    Implements a priority queue data structure. Each inserted item
    has a priority associated with it and the client is usually interested
    in quick retrieval of the lowest-priority item in the queue. This
    data structure allows O(1) access to the lowest-priority item.
    
    Note that this PriorityQueue does not allow you to change the priority
    of an item.  However, you may insert the same item multiple times with
    different priorities.
  """  
  def  __init__(self):  
    self.heap = []
    
  def push(self, item, priority):
      pair = (priority,item)
      heapq.heappush(self.heap,pair)

  def pop(self):
      (priority,item) = heapq.heappop(self.heap)
      return item
  
  def isEmpty(self):
    return len(self.heap) == 0



class SpaceStation:

    def __init__(self, size = 5):
        self.size = size
        midpoint = round(float(size) / 2.0 + .01) - 1
        self.airlock = [midpoint, midpoint]
    
    def getMoves(self, game, i):
        y = game[i][0]
        x = game[i][1]
        successors = []
        # check north
        loop = True
        yt = y - 1
        if [yt, x] in game:
            loop = False
        while loop and yt > 0:
            if [yt - 1, x] in game:
                tmp = list(game)
                if [yt, x] == self.airlock and i != 0:
                    tmp.pop(i)
                else:
                    tmp[i] = [yt, x]
                successors.append([tmp, [i, 'North']])
                loop = False
            yt -= 1

        # check south
        loop = True
        yt = y + 1
        if [yt, x] in game:
            loop = False
        while loop and yt < self.size:
            if [yt + 1, x] in game:
                tmp = list(game)
                if [yt, x] == self.airlock and i != 0:
                    tmp.pop(i)
                else:
                    tmp[i] = [yt, x]
                successors.append([tmp, [i, 'South']])
                loop = False
            yt += 1


        # check east
        loop = True
        xt = x + 1
        if [y, xt] in game:
            loop = False
        while loop and xt < self.size:
            if [y, xt + 1] in game:
                tmp = list(game)
                if [y, xt] == self.airlock and i != 0:
                    tmp.pop(i)
                else:
                    tmp[i] = [y, xt]
                successors.append([tmp, [i, 'East']])
                loop = False
            xt += 1


        # check west
        loop = True
        xt = x - 1
        if [y, xt] in game:
            loop = False
        while loop and xt > 0:
            if [y, xt - 1] in game:
                tmp = list(game)
                if [y, xt] == self.airlock and i != 0:
                    tmp.pop(i)
                else:
                    tmp[i] = [y, xt]
                successors.append([tmp,  [i, 'West']])
                loop = False
            xt -= 1

        return successors
            

    def getSuccessors(self, game):
        """ given a game in the form of
        [[1,1], [0, 1], [0, 2], [3, 3], [4,1]]
        will return a list of successors"""
        
        successors = []
        for i in range(len(game)):
            successors += self.getMoves(game, i)
        return successors


    def getSolution(self, game):
        print "begin"
        
        """orienation holds initial locations of pieces"""
        orientation = game
        """frontier is stored in frontierQueue"""
        frontierQueue = PriorityQueue()
        """explored states are stored in a dictionary"""
        exploredStates = {}
        """moves to be stored for each explored state"""
        movesThisFar = []
        """dictionary to hold each state as a key to the moves needed"""
        statesDictionary = {}
        """list to hold the actions for each state"""
        actionsList = []
        """has the goal been reached?"""
        reachedGoal = False
        
        print "init orientation is", orientation
        print "carbon based is at", orientation[0]
        """get successors of start state"""
        successors = self.getSuccessors(orientation)
        print "initial successors are",successors
        print ""
        print ""
        """push initial successors onto the frontier queue"""
        for i in successors:
            movesThisFar=copy.deepcopy(actionsList)
            cat = i[1]
            movesThisFar.append([cat[0],cat[1]])
            i[1]=copy.deepcopy(movesThisFar)
            """add the frontier state to the stateDictionary"""
            state = str(i[0])
            statesDictionary[state]=movesThisFar
            frontierQueue.push(i,0)
            
        """put initial state in the explored states dictionary"""
        exploredStates[str(movesThisFar)]=orientation
        """put the initial state in the states dictionary"""
        statesDictionary[str(orientation)]=[]
        #while the goal state has not been reached
        while orientation[0] != spaceStation.airlock: 
            
            #hum
            prevActions = copy.deepcopy(actionsList)
            
            """put the state in the explored states dictionary"""
            exploredStates[str(movesThisFar)]=orientation
            
            
            """"get the next state off the frontier"""
            frontierNode = frontierQueue.pop()
            
            """get the actions and orientation of that frontier state"""
            reset = str(frontierNode[0])
            #print "states dictionary", statesDictionary
            actionsList = copy.deepcopy(statesDictionary[reset])#actions to this point
            
            
            orientation =frontierNode[0]#pieces orientation
            #print "the current orientation is", orientation
            #print "the current actions list is", actionsList
            
            """check is goal?"""
            if (orientation[0] == spaceStation.airlock):
                reachedGoal == True
                break
                
            
            """generate successors""" 
            successors = self.getSuccessors(orientation)    
            
            """push successors onto the frontier queue if unexplored"""
            for i in successors:
                explored = False
                state=i[0]
                counter = 0
                """for each item in the explored states"""
                for k in exploredStates:
                    
                    """if we have seen that state before we mark it"""
                    if(state == exploredStates[k]):
                        explored = True
                        
                    counter = counter +1
                    
                """if we have not seen this state before"""
                if(explored == False):
                    """add the new action of this frontier state to the actions list"""
                    movesThisFar=copy.deepcopy(actionsList)
                    movesThisFar.append(i[1])
                    i[1]=copy.deepcopy(movesThisFar)
                    """add the frontier state to the stateDictionary"""
                    state = str(i[0])
                    statesDictionary[state]=movesThisFar
                    
                    frontierQueue.push(i,0)
                    
        
        #solution = statesDictionary[str(orientation)]
        solution = actionsList
        print "The solution set is : "
        return solution        


# your code should pass these tests

# The following is one solution for game 1. There is at least one more.
#solution1 = [[0, 'South'], [0, 'East'], [0, 'North'], [1, 'South'], [3, 'West'], [0, 'South']]
game1 =  [[1,1], [0, 1], [0, 2], [3, 3], [4,1]]
firstGamePositions = "The starting positions for the first game are: [[1,1], [0, 1], [0, 2], [3, 3], [4,1]] "
#solution2 = [[2, 'West'], [5, 'North'], [5, 'East'], [5, 'South'], [5, 'West'], [4, 'North'], [4, 'East'], [0, 'North'], [0, 'West']]
game2 = [[3,3], [0,0], [0, 2], [1, 4], [2, 0], [4, 1]]
secondGamePositions = "The starting positions for the second game are: [[3,3], [0,0], [0, 2], [1, 4], [2, 0], [4, 1]] "

spaceStation = SpaceStation()
print "solution 1:"
print spaceStation.getSolution(game1)
firstGameSolution = spaceStation.getSolution(game1)
print ""
spaceStation = SpaceStation()
print "solution 2:"
print spaceStation.getSolution(game2)
secondGameSolution = spaceStation.getSolution(game2)
print ""

#show output with tkinter
root = Tk()

labelOne = Label(root, text = firstGamePositions,)
labelOne.pack() #add to screen
#label for first board
BoardOneText = " +---+---+---+---+---+ \n |      |   1   |   2   |       |      | \n +---+---+---+---+---+ \n |       |   X   |       |       |     | \n +---+---+---+---+---+ \n |       |       |   O   |       |     | \n +---+---+---+---+---+ \n |       |       |       |   3   |     | \n  +---+---+---+---+---+ \n |       |   4   |       |       |      |\n  +---+---+---+---+---+"
labelBoardOne = Label(root,text=BoardOneText,fg="red",justify=LEFT)
labelBoardOne.pack()
#end board one

labelTwo = Label (root, text = "The first game solution set is: ", justify=RIGHT)
labelTwo.pack() #add to screen
solution1LB = Listbox(root) #create listbox
for item in firstGameSolution:
    solution1LB.insert(END,item)
solution1LB.pack() #add listbox

labelThree = Label(root, text = secondGamePositions)
labelThree.pack() #add to screen
#add second board
BoardTwoText = " +---+---+---+---+---+ \n "
BoardTwoText = BoardTwoText + "|   1   |       |   4   |       |       | \n"
BoardTwoText = BoardTwoText + "+---+---+---+---+---+ \n"
BoardTwoText = BoardTwoText + "|       |       |         |       |   5   | \n"
BoardTwoText = BoardTwoText + "+---+---+---+---+---+ \n"
BoardTwoText = BoardTwoText + "|   2   |       |   O   |       |       | \n"
BoardTwoText = BoardTwoText + "+---+---+---+---+---+ \n"
BoardTwoText = BoardTwoText + "|       |       |         |   X   |       | \n"
BoardTwoText = BoardTwoText + "+---+---+---+---+---+ \n"
BoardTwoText = BoardTwoText + "|       |   3   |        |       |       |\n"
BoardTwoText = BoardTwoText + "+---+---+---+---+---+ "
labelBoardTwo = Label(root,text=BoardTwoText,fg="red" ,justify=LEFT)
labelBoardTwo.pack()
#end second board
labelFour = Label (root, text = "The second game solution set is: ",justify=RIGHT)
labelFour.pack() #add to screen
solution2LB = Listbox(root) #create listbox
for item in secondGameSolution:
    solution2LB.insert(END,item)
solution2LB.pack()

root.mainloop()
