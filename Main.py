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
  mlController.learn()
  mlController.executeFinal()

def playMode():
  writeBeginning = 1

  while True:
    game = Threes()
    game.play()
    writeBeginning += 10

def main():
  parser = argparse.ArgumentParser(description='Run threes game.')
  parser.add_argument("-m", metavar="--mode", default="p", type=str, help="Mode")
  parser.add_argument("-t", metavar="--vtable", default=None, type=str, help="Vtable. Select file in 'vTables' or 'last' to continue with most recent file")
  parser.add_argument("-i", metavar="--inline", default=True, type=int, help="Print inline")

  args = parser.parse_args()
  printer.setInlineMode(args.i)

  if args.m == "m":
    mlMode(args.t)
  elif args.m == "p":
    playMode()
  else:
    print("Invalid mode")

def exitGraceful(signal, frame):
  global mlController
  if mlController:
    mlController.executeFinal()

  printer.end()
  sys.exit(0)

if __name__ == "__main__":
  signal.signal(signal.SIGINT, exitGraceful)
  main()
  curses.endwin()
