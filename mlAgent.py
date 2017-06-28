import random
import sys
import copy
import operator
from random import Random
import datetime
import time

from constants import *

class Observation:
  worldState = []
  availableActions = []
  hierarchy = {}
  isTerminal = None
  def __init__(self, state=None, actions=None, hierarchy=None, isTerminal=None):
    if state != None:
      self.worldState = state

    if actions != None:
      self.availableActions = actions

    if hierarchy != None:
      self.hierarchy = hierarchy

    if isTerminal != None:
      self.isTerminal = isTerminal

class Agent:
  # Q-learning stuff: Step size, epsilon, gamma, learning rate
  epsilon = 0.5
  gamma = 0.9
  learningRate = 1.0
  numSteps = 100000

  # Observation tracking
  currentObs = None
  lastObservation=Observation()

  # Total reward
  totalReward = 0.0
  count = 0

  # Constructor, takes a reference to an Environment
  def __init__(self, env):
    # Initialize value table
    self.v_table={}

    # Set dummy action and observation
    self.lastObservation=Observation()

    # Set the environment
    self.gridEnvironment = env

    # Get first observation and start the environment
    self.initialObs = self.gridEnvironment.env_start()
    self.initializeVtableStateEntry(self.initialObs.worldState)

  # Make an empty row in the v table with the state as key.
  def initializeVtableStateEntry(self, state):
    if tuple(state) not in self.v_table.keys():
      self.v_table[tuple(state)] = NUM_ACTIONS*[0.0]

  # Once learning is done, use this to run the agent
  # observation is the initial observation
  def executePolicy(self, writeFile=False):
    if writeFile:
      dateString = str(datetime.datetime.now().isoformat())
      dateString = dateString.replace("-","_")
      dateString = dateString.split(".")[0]
      dateString = dateString.replace(":",".")
      dateString = dateString.replace("T", "-")
      outputfile = open("output/" + dateString + ".txt", "w+")

    # History stores up list of actions executed
    history = []

    # Start the counter
    self.count = 0

    # reset total reward
    self.totalReward = 0.0

    # Copy the initial observation
    self.workingObservation = self.copyObservation(self.initialObs)

    # Make sure the value table has the starting observation
    self.initializeVtableStateEntry(self.workingObservation.worldState)

    if writeFile:
      outputfile.write("START\n")
      outputfile.write("LR:" + str(self.learningRate) + "\n")
      outputfile.write("Gamma:" + str(self.gamma) + "\n\n")

    # While a terminal state has not been hit and the counter hasn't expired, take the best action for the current state
    while not self.workingObservation.isTerminal and self.count < self.numSteps:
      # Get the best action for this state
      newAction = self.greedy(self.workingObservation)
      history.append((newAction, self.workingObservation.worldState))

      if writeFile:
        outputfile.write("state: " + str(self.workingObservation.worldState) + "\n")
        outputfile.write("action: " + str(newAction) + "\n")

      # execute the step and get a new observation and reward
      currentObs, reward = self.gridEnvironment.env_step(newAction)
      if writeFile:
        outputfile.write("reward:" + str(reward) + "\n")
        outputfile.write("total reward:" + str(self.totalReward + reward) + "\n")
        outputfile.write(str(self.gridEnvironment)+"\n")
        outputfile.write("\n")

      self.totalReward = self.totalReward + reward
      self.workingObservation = copy.deepcopy(currentObs)

      # increment counter
      self.count += 1

    if writeFile:
      outputfile.write("END")

    return history

  # q-learning implementation
  def qLearn(self):
    # copy the initial observation
    self.workingObservation = self.copyObservation(self.initialObs)

    # start the counter
    self.count = 0

    # reset total reward
    self.totalReward = 0.0

    # while terminal state not reached and counter hasn't expired, use epsilon-greedy search
    while not self.workingObservation.isTerminal and self.count < self.numSteps:

      # Make sure table is populated correctly
      self.initializeVtableStateEntry(self.workingObservation.worldState)

      # Take the epsilon-greedy action
      nextAction = self.egreedy(self.workingObservation)
      currentObs, reward = self.gridEnvironment.env_step(nextAction)

      # Make sure table is populated correctly
      self.initializeVtableStateEntry(currentObs.worldState)

      # update the value table
      self.updateVtable(
        tuple(currentObs.worldState),
        tuple(self.workingObservation.worldState),
        nextAction,
        reward,
        currentObs.isTerminal,
        currentObs.availableActions
      )

      self.workingObservation = self.copyObservation(currentObs)

      self.count += 1
      self.totalReward += reward

    # Done learning, reset environment
    self.gridEnvironment.env_reset()

  ### Update the v_table during q-learning.
  def updateVtable(self, newState, lastState, action, reward, terminal, availableActions):
    r_tp1 = float(reward)
    Q_st_at = float(self.v_table[tuple(lastState)][action])
    lr = float(self.learningRate)
    y = float(self.gamma)

    # Q(st, at) = Q(st,at) + lr*(rt+1 + y*max(Q(st+1, a')) - Q(st, at))
    if not terminal:
      # Calculate all rewards for potential actions
      Q_stp1_a = []
      for potentialAction in availableActions:
        Q_stp1_a.append(float(self.v_table[tuple(newState)][potentialAction]))

      # Calculate new val
      newVal = Q_st_at + lr*(r_tp1 + y*max(Q_stp1_a) - Q_st_at)

    # Q(st, at) = Q(st, at) + lr*(rt+1 - Q(st,at))
    else:

      # Calculate new val
      newVal = Q_st_at + lr*(r_tp1 - Q_st_at)

    # Update vtable
    self.v_table[tuple(lastState)][action] = newVal

  def egreedy(self, observation):
    self.initializeVtableStateEntry(observation.worldState)

    # Mark impossible moves
    impossibleMoves = self.gridEnvironment.board.impossibleMoves()
    for impossibleMove in impossibleMoves:
      self.v_table[tuple(observation.worldState)][impossibleMove] = -1

    # Choose random action
    possibleMoves = self.gridEnvironment.board.possibleMoves()
    if random.uniform(0,1) < self.epsilon:
      return random.choice(possibleMoves)

    # Choose greedy option
    else:
      return self.greedy(observation)

  def greedy(self, observation):
    self.initializeVtableStateEntry(observation.worldState)

    # Mark impossible moves
    impossibleMoves = self.gridEnvironment.board.impossibleMoves()
    for impossibleMove in impossibleMoves:
      self.v_table[tuple(observation.worldState)][impossibleMove] = -1

    rewards = []
    for actionVal in range(0, NUM_ACTIONS):
      rewards.append(self.v_table[tuple(observation.worldState)][actionVal])

    return rewards.index(max(rewards))

  # Reset the agent
  def agent_reset(self):
    self.lastObservation = Observation()
    self.initialObs = self.gridEnvironment.env_start()

  # Create a copy of the observation
  def copyObservation(self, obs):
    returnObs =  Observation()
    if obs.worldState != None:
      returnObs.worldState = obs.worldState[:]

    if obs.availableActions != None:
      returnObs.availableActions = obs.availableActions[:]

    if obs.isTerminal != None:
      returnObs.isTerminal = obs.isTerminal

    return returnObs
