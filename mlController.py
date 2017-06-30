from mlAgent import *
from threes import *
from utils import *
import pickle

class MLController():
  def __init__(self, inlineMode, vTable={}):
    self.trainingEpisodes = 1000
    self.trainingReportRate = 1

    self.largestMoveCount = 0
    self.largestReward = 0

    self.mlAgent = MLAgent(Threes(), vTable)
    self.startVtableSize = len(self.mlAgent.vTable)

  def learn(self):
    for i in range(self.trainingEpisodes):
      # Print iteration info
      printer.printLine(0,"Iteration: " + str(i))
      printer.printLine(1,"V Table size: " + str(self.startVtableSize) + "->" + str(len(self.mlAgent.vTable)))
      printer.printLine(2,"Highest Moves: " + str(self.largestMoveCount))

      # Train
      self.mlAgent.qLearn()

      # Report a test
      if i % self.trainingReportRate == 0:
        self.test()

      # Update longest game
      if self.mlAgent.count > self.largestMoveCount:
          self.largestMoveCount = self.mlAgent.count

  def test(self):
    # Test
    self.mlAgent.executePolicy()

    # Update best board
    if self.mlAgent.totalReward > self.largestReward:
      self.largestReward = self.mlAgent.totalReward

      # Best board
      printer.printLine(4, "Best Board")
      printer.printLine(5, str(self.mlAgent.gameEnv.board))
      printer.printLine(11, "Moves: " + str(self.mlAgent.count))

  def executeFinal(self):
    # Execute one last time and write to file
    self.mlAgent.executePolicy(writeFile=True)

    # Write vTable to start from later
    outputfile = createTimeStampedFile("vTables", ext="data")
    pickle.dump(self.mlAgent.vTable, outputfile)
    outputfile.close()
