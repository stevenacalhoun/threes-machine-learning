import sys
from Observation import *
from Reward import *
from Action import *
from Agent import *
from Environment import *
import numpy
import time

def main():
  gammas = [1.0,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1]
  LRs = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]

  start = time.time()
  i = 0
  results = []
  currentMax = 0
  maxLR = 0
  maxGamma = 0
  for gamma in gammas:
    for LR in LRs:
      i+=1
      trialStart = time.time()
      maxr = runTraining(gamma, LR)
      print
      print "Result " + str(i)
      print "Gamma: " + str(gamma)
      print "LR: " + str(LR)
      print "Reward: " + str(maxr)
      print "Trial time: " + str(time.time() - trialStart)
      print "Total time: " + str(time.time() - start)

      if maxr > currentMax:
        currentMax = maxr
        maxLR = LR
        maxGamma = gamma

      print
      print "Best"
      print "Reward: " + str(currentMax)
      print "LR: " + str(maxLR)
      print "Gamma: " + str(maxGamma)
      print
      print

      results.append({"reward": maxr, "gamma": gamma, "LR": LR})
  print results

def runTraining(gamma, LR):
  # Training episodes
  episodes = 500

  # how often to report training results
  trainingReportRate = 100

  # play the interactive game?
  # 0: human does not play
  # 1: human plays as the bot
  # 2: human plays as the enemy
  play = 2

  #Max reward received in any iteration
  maxr = None

  # Set up environment for initial training
  gridEnvironment = Environment()
  gridEnvironment.randomStart = False
  gridEnvironment.enemyMode = 2
  gridEnvironment.verbose = 0

  # Set up agent
  gridAgent = Agent(gridEnvironment)
  gridAgent.verbose = False
  gridAgent.gamma = gamma
  gridAgent.learningRate = LR

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
    if maxr == None or totalr > maxr:
      maxr = totalr

    if i % trainingReportRate == 0:
      print "iteration:", i, "total reward", totalr, "max reward:", maxr


  # Reset the environment for policy execution
  gridEnvironment.verbose = 0
  gridEnvironment.randomStart = False
  gridEnvironment.enemyMode = 1
  gridAgent.verbose = True

  # print "Execute Policy"
  gridAgent.agent_reset()
  gridAgent.executePolicy(gridAgent.initialObs, writeFile=True)
  # print "total reward", gridAgent.totalReward

  return maxr

if __name__ == "__main__":
  main()
