import sys
from mlAgent import *
from threes import *
import numpy
import time

class MLController():
  def __init__(self):
    self.trainingEpisodes = 10
    self.trainingReportRate = 1

    self.largestReward = 0
    self.largestBoardValue = 0
    self.largestMoveCount = 0

    self.gridAgent = Agent(Threes())

  def runLearning(self):
    # This is where learning happens
    for i in range(self.trainingEpisodes):
      # Train
      self.gridAgent.agent_reset()
      self.gridAgent.qLearn()

      # Test
      self.gridAgent.agent_reset()
      self.gridAgent.executePolicy()

      if self.gridAgent.count > self.largestMoveCount:
        self.largestMoveCount = self.gridAgent.count

      if self.gridAgent.gridEnvironment.board.getLargestVal() > self.largestBoardValue:
        self.largestBoardValue = self.gridAgent.gridEnvironment.board.getLargestVal()

      if self.largestReward == None or self.gridAgent.totalReward > self.largestReward:
        self.largestReward = self.gridAgent.totalReward
        print self.gridAgent.gridEnvironment.board
        print "max reward:", self.largestReward, " largest val ", self.largestBoardValue, " largest count: ", self.largestMoveCount

      if i % self.trainingReportRate == 0:
        print "iteration:", i

  def executeFinal(self):
    print "Execute Policy"
    self.gridAgent.agent_reset()
    self.gridAgent.executePolicy(writeFile=True)
    print "total reward", self.gridAgent.totalReward
