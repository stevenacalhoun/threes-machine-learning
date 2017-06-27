import sys
from Observation import *
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
largestCount = 0

# Set up agent
gridAgent = Agent(Threes())

# This is where learning happens
for i in range(episodes):
  # Train
  gridAgent.agent_reset()
  gridAgent.qLearn()

  # Test
  gridAgent.agent_reset()
  gridAgent.executePolicy()

  if gridAgent.count > largestCount:
    largestCount = gridAgent.count

  if gridAgent.gridEnvironment.board.getLargestVal() > largestVal:
    largestVal = gridAgent.gridEnvironment.board.getLargestVal()

  if maxr == None or gridAgent.totalReward > maxr:
    maxr = gridAgent.totalReward
    print gridAgent.gridEnvironment.board
    print "max reward:", maxr, " largest val ", largestVal, " largest count: ", largestCount

  if i % trainingReportRate == 0:
    print "iteration:", i

print "Execute Policy"
gridAgent.agent_reset()
gridAgent.executePolicy(writeFile=True)
print "total reward", gridAgent.totalReward
