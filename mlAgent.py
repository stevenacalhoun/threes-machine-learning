import random
import copy
import datetime

from constants import *
from utils import *

class MLAgent:
  # Q-learning stuff: Step size, epsilon, gamma, learning rate
  epsilon = 0.5
  numSteps = 100000

  gamma = 0.99
  learningRate = 1.0

  # Constructor, takes a reference to an Environment
  def __init__(self, gameEnv, vTable):
    self.vTable = vTable
    self.gameEnv = gameEnv
    self.restart()

  # Make an empty row in the v table with the state as key.
  def initializeVtableStateEntry(self, state):
    if tuple(state) not in self.vTable.keys():
      self.vTable[tuple(state)] = NUM_ACTIONS*[0.0]

      # Mark impossible moves
      impossibleMoves = self.gameEnv.board.impossibleMoves()
      for impossibleMove in impossibleMoves:
        self.vTable[tuple(state)][impossibleMove] = -1

  # Execute policy in vtable choosing only the best moves
  def executePolicy(self, writeFile=False):
    self.restart()

    if writeFile:
      outputfile = createTimeStampedFile("output")
      outputfile.write("LR:" + str(self.learningRate) + "\n")
      outputfile.write("Gamma:" + str(self.gamma) + "\n\n")

    # While a terminal state has not been hit and the counter hasn't expired, take the best action for the current state
    while not self.workingState[-1] and self.count < self.numSteps:
      # Get the best action for this state
      newAction = self.greedy(self.workingState)
      currentState, reward = self.gameEnv.step(newAction)

      self.totalReward = self.totalReward + reward
      self.workingState = currentState[:]

      # increment counter
      self.count += 1

      # Write data
      if writeFile:
        outputfile.write("state: " + str(self.workingState) + "\n")
        outputfile.write("action: " + str(newAction) + "\n")
        outputfile.write("reward:" + str(reward) + "\n")
        outputfile.write("total reward:" + str(self.totalReward + reward) + "\n")
        outputfile.write(str(self.gameEnv)+"\n")
        outputfile.write("\n")

  # Q-Learning
  def qLearn(self):
    self.restart()

    # while terminal state not reached and counter hasn't expired, use epsilon-greedy search
    while not self.workingState[-1] and self.count < self.numSteps:
      # Take the epsilon-greedy action
      nextAction = self.egreedy(self.workingState)
      currentState, reward = self.gameEnv.step(nextAction)

      # Update the vtable
      self.initializeVtableStateEntry(currentState)
      self.updateVtable(
        tuple(currentState),
        tuple(self.workingState),
        nextAction,
        reward,
        currentState[-1],
        [0,1,2,3]
      )

      self.totalReward += reward
      self.workingState = currentState[:]

      self.count += 1

  # Update the vTable
  def updateVtable(self, newState, lastState, action, reward, terminal, availableActions):
    r_tp1 = float(reward)
    Q_st_at = float(self.vTable[tuple(lastState)][action])
    lr = float(self.learningRate)
    y = float(self.gamma)

    # Q(st, at) = Q(st,at) + lr*(rt+1 + y*max(Q(st+1, a')) - Q(st, at))
    if not terminal:
      # Calculate all rewards for potential actions
      Q_stp1_a = []
      for potentialAction in availableActions:
        Q_stp1_a.append(float(self.vTable[tuple(newState)][potentialAction]))

      newVal = Q_st_at + lr*(r_tp1 + y*max(Q_stp1_a) - Q_st_at)

    # Q(st, at) = Q(st, at) + lr*(rt+1 - Q(st,at))
    else:
      newVal = Q_st_at + lr*(r_tp1 - Q_st_at)

    # Update vtable
    self.vTable[tuple(lastState)][action] = newVal

  # Choose best option or random choice
  def egreedy(self, state):
    self.initializeVtableStateEntry(state)

    # Explore or be greedy
    if random.uniform(0,1) < self.epsilon:
      return random.choice(self.gameEnv.board.possibleMoves())
    else:
      return self.greedy(state)

  # Choose best option
  def greedy(self, state):
    self.initializeVtableStateEntry(state)
    return self.vTable[tuple(state)].index(max(self.vTable[tuple(state)]))

  # Restart counts, observations, and environments
  def restart(self):
    self.count = 0
    self.totalReward = 0.0
    self.workingState = self.gameEnv.start()[:]
    self.initializeVtableStateEntry(self.workingState)
