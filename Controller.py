import sys
from Observation import *
from Reward import *
from Action import *
from Agent import *
from ThreesGame import *
import numpy
import time

# Training episodes
episodes = 10000

# how often to report training results
trainingReportRate = 10

# Max reward received in any iteration
maxr = None
largestVal = None

# Set up environment for initial training
gridEnvironment = Threes()
gridEnvironment.verbose = 0

# Set up agent
gridAgent = Agent(gridEnvironment)
gridAgent.verbose = False

# This is where learning happens
for i in range(episodes):
  # Train
  gridAgent.agent_reset()
  gridAgent.qLearn(gridAgent.initialObs)

  # Test
  gridAgent.agent_reset()
  gridAgent.executePolicy(gridAgent.initialObs)

  # Report
  totalr = gridAgent.totalReward
  currentLargestVal = gridAgent.gridEnvironment.board.getLargestVal()

  if currentLargestVal > largestVal:
    largestVal = currentLargestVal


  if maxr == None or totalr > maxr:
    maxr = totalr
    print gridAgent.gridEnvironment.board
    print "max reward:", maxr, " largest val ", largestVal

  if i % trainingReportRate == 0:
    print "iteration:", i

# Reset the environment for policy execution
gridEnvironment.verbose = 0
gridEnvironment.randomStart = False
gridEnvironment.enemyMode = 1
gridAgent.verbose = True

print "Execute Policy"
gridAgent.agent_reset()
gridAgent.executePolicy(gridAgent.initialObs, writeFile=True)
print "total reward", gridAgent.totalReward
