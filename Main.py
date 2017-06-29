from threes import *
from mlController import *

import subprocess
import curses
import signal
import argparse
import sys
import os
import glob
import pickle

mlController = None

def getMostRecentVTableFile():
  return max(glob.iglob('vTables/*'), key=os.path.getctime)

def loadVTableFile(fileName):
  if fileName == "last":
    fileName = getMostRecentVTableFile()

  with open(fileName, 'r') as f:
    data = pickle.load(f)

  return data

def mlMode(vTableFile):
  global mlController
  if vTableFile:
    vTable = loadVTableFile(vTableFile)
  else:
    vTable = {}

  mlController = MLController(vTable)

  # Learn and execute
  mlController.runLearning()
  mlController.executeFinal()

def playMode(vTable):
  writeBeginning = 1
  printMode = 0

  while True:
    game = Threes(writeBeginning=writeBeginning, printMode=1)
    game.play()
    writeBeginning += 10

def main():
  parser = argparse.ArgumentParser(description='Run threes game.')
  parser.add_argument("-m", metavar="--mode", type=str, help="Mode")
  parser.add_argument("-t", metavar="--vtable", type=str, help="Vtable. Select file in 'vTables' or 'last' to continue with most recent file")

  args = parser.parse_args()

  if args.m == "m":
    mlMode(args.t)
  elif args.m == "p":
    playMode()
  else:
    print("Need to select a mode")

def exitGraceful(signal, frame):
  global mlController
  if mlController:
    mlController.executeFinal()

  curses.endwin()
  sys.exit(0)

if __name__ == "__main__":
  signal.signal(signal.SIGINT, exitGraceful)
  main()
  curses.endwin()
