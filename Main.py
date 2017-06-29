from threes import *
from mlController import *

import argparse

def mlMode():
  mlController = MLController()

  # Learn and execute
  mlController.runLearning()
  mlController.executeFinal()

def playMode():
  writeBeginning = 1
  printMode = 0

  while True:
    game = Threes(writeBeginning=writeBeginning, printMode=1)
    game.play()
    writeBeginning += 10

def main():
  parser = argparse.ArgumentParser(description='Run threes game.')
  parser.add_argument("-m", metavar="--mode", type=str, help="Mode")

  args = parser.parse_args()

  if args.m == "m":
    mlMode()
  elif args.m == "p":
    playMode()
  else:
    print("Need to select a mode")

if __name__ == "__main__":
  main()
