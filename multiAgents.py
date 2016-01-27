# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        "*** YOUR CODE HERE ***"
        score = 0
        for pos in successorGameState.getGhostPositions():
            dis = manhattanDistance(pos, newPos)
            if (dis <= 1): score = -1000
            else: score -= 5.0/dis 
        for pos in  newFood.asList():
            dis = (manhattanDistance(pos, newPos))
            if dis == 0:
                score += 100
            else:
                score += 5.0/dis
                
        for ghost in newGhostStates:
            score += ghost.scaredTimer*10
        if (currentGameState.getNumFood() > successorGameState.getNumFood()):
            score += 10

        for capsule in currentGameState.getCapsules():
          dis=manhattanDistance(capsule,newPos)
          if(dis==0):
            score += 200
          else:
            score+=5.0/dis
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        actions = self.maxvalue(gameState, self.depth)[1]
        return actions

    def maxvalue(self,gameState,dep):
        if dep ==0 or gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState),None)
        act = gameState.getLegalActions(0)
        res = []
        for action in act:
            res.append(self.minvalue(gameState.generateSuccessor(0, action),dep,1)[0])
        
        v = max(res)
        ind = [ind for ind in range(len(res)) if res[ind] == v]
        actions = act[ind[0]]
        return (v,actions)
    
    def minvalue(self,gameState,dep,AgentIndex):
        if dep ==0 or gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState),None)

        act = gameState.getLegalActions(AgentIndex)
        res = []
        for action in act:
            if (AgentIndex == gameState.getNumAgents()-1 ):    
                res.append(self.maxvalue(gameState.generateSuccessor(AgentIndex,action),dep-1)[0])
            else:
                res.append(self.minvalue(gameState.generateSuccessor(AgentIndex,action),dep,AgentIndex+1)[0])
        v = min(res)
        ind = [ind for ind in range(len(res)) if res[ind] == v]
        actions = act[ind[0]]
        return (v,actions)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        actions = self.maxvalue(gameState, self.depth,-float("inf"),float("inf"))[1]
        
        return actions
        #util.raiseNotDefined()

    def maxvalue(self,gameState,dep,alpha,beta):
        if dep ==0 or gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState),None)
        act = gameState.getLegalActions(0)
        res = []
        temp = -float('inf')
        for action in act:
            temp = max(temp,self.minvalue(gameState.generateSuccessor(0, action),dep,1,alpha,beta)[0])
            res.append(temp)
            if (temp>beta): return (temp,action)
            alpha = max(alpha,temp)
        v = max(res)
        ind = [ind for ind in range(len(res)) if res[ind] == v]
        actions = act[ind[0]]
        return (v,actions)
    
    def minvalue(self,gameState,dep,AgentIndex,alpha,beta):
        if dep ==0 or gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState),None)

        act = gameState.getLegalActions(AgentIndex)
        res = []
        temp = float('inf')
        for action in act:
            if (AgentIndex == gameState.getNumAgents()-1 ):    
                temp = min(temp,self.maxvalue(gameState.generateSuccessor(AgentIndex,action),dep-1,alpha,beta)[0])
                res.append(temp)
                if (temp<alpha): return (temp,action)
                beta = min(beta,temp)
            else:
                temp = min(temp,self.minvalue(gameState.generateSuccessor(AgentIndex,action),dep,AgentIndex+1,alpha,beta)[0])
                res.append(temp)
                if (temp<alpha): return (temp,action)
                beta = min(beta,temp)                
        v = min(res)
        ind = [ind for ind in range(len(res)) if res[ind] == v]
        actions = act[ind[0]]
        #print v
        return (v,actions)    
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.maxvalue(gameState,self.depth)[1]
        
    def maxvalue(self,gameState,dep):
        if dep==0:
            return (self.evaluationFunction(gameState),None)
        act = gameState.getLegalActions(0)
        if len(act)==0:
            return (self.evaluationFunction(gameState),None)
        res = []
        temp = -float('inf')
        for action in act:
            temp = max(temp,self.exp(gameState.generateSuccessor(0, action),1,dep)[0])
            res.append(temp)
        v = max(res)
        ind = [ind for ind in range(len(res)) if res[ind] == v]
        actions = act[ind[0]]
        return (v,actions)

    def exp(self,gameState,AgentIndex,dep):
        act = gameState.getLegalActions(AgentIndex)
        if len(act)==0:
            return (self.evaluationFunction(gameState),None)
        res = []
        temp = float('inf')
        tot = 0
        for action in act:
            if (AgentIndex == gameState.getNumAgents()-1 ):    
                temp = self.maxvalue(gameState.generateSuccessor(AgentIndex,action),dep-1)[0]
                res.append(temp)
            else:
                temp = self.exp(gameState.generateSuccessor(AgentIndex,action),AgentIndex+1,dep)[0]
                res.append(temp)
            tot += temp*1.0/len(act)   
        v = min(res)
        ind = [ind for ind in range(len(res)) if res[ind] == v]
        actions = act[ind[0]]
        return (tot,actions)
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
    score = 0
    min_dis = float('inf')
    for pos in  newFood.asList():
        temp = manhattanDistance(pos, newPos)
        if temp < min_dis:
            min_dis = temp
    if (min_dis < float('inf')):
        score -= min_dis

    score -= 1000*currentGameState.getNumFood()            
    score -= len(currentGameState.getCapsules())*10
    for pos in currentGameState.getGhostPositions():
        dis = manhattanDistance(pos, newPos)
        if (dis <= 3): score = -float('inf')
    score += currentGameState.getScore()*10
    return score        
    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

