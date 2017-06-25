import random
import curses
import time

from math import log
from math import pow

from Observation import *
from Action import *
from Reward import *

def printMoveMatrix(matrix):
  strResp = ""
  for i,bool in enumerate(matrix):
    if i % 4==0:
      strResp += "\n"
    if bool:
      strResp += "1 "
    else:
      strResp += "0 "
  print strResp
  print

NUM_ROWS = 4
NUM_COLS = 4
NUM_TILES = NUM_COLS*NUM_ROWS

UP = 'Up'
RIGHT = 'Right'
DOWN = 'Down'
LEFT = 'Left'
ALL_MOVES = [UP,RIGHT,DOWN,LEFT]

ROW_1_INDECIES = [0,  1,  2,  3]
ROW_2_INDECIES = [4,  5,  6,  7]
ROW_3_INDECIES = [8,  9,  10, 11]
ROW_4_INDECIES = [12, 13, 14, 15]
ROWS = [ROW_1_INDECIES,ROW_2_INDECIES,ROW_4_INDECIES]

COL_1_INDECIES = [ROW_1_INDECIES[0], ROW_2_INDECIES[0], ROW_3_INDECIES[0], ROW_4_INDECIES[0]]
COL_2_INDECIES = [ROW_1_INDECIES[1], ROW_2_INDECIES[1], ROW_3_INDECIES[1], ROW_4_INDECIES[1]]
COL_3_INDECIES = [ROW_1_INDECIES[2], ROW_2_INDECIES[2], ROW_3_INDECIES[2], ROW_4_INDECIES[2]]
COL_4_INDECIES = [ROW_1_INDECIES[3], ROW_2_INDECIES[3], ROW_3_INDECIES[3], ROW_4_INDECIES[3]]
COLS = [COL_1_INDECIES,COL_2_INDECIES,COL_3_INDECIES,COL_4_INDECIES]

UP_ORDER = []
UP_ORDER.extend(ROW_1_INDECIES)
UP_ORDER.extend(ROW_2_INDECIES)
UP_ORDER.extend(ROW_3_INDECIES)
UP_ORDER.extend(ROW_4_INDECIES)

DOWN_ORDER = []
DOWN_ORDER.extend(ROW_4_INDECIES)
DOWN_ORDER.extend(ROW_3_INDECIES)
DOWN_ORDER.extend(ROW_2_INDECIES)
DOWN_ORDER.extend(ROW_1_INDECIES)

LEFT_ORDER = []
LEFT_ORDER.extend(COL_1_INDECIES)
LEFT_ORDER.extend(COL_2_INDECIES)
LEFT_ORDER.extend(COL_3_INDECIES)
LEFT_ORDER.extend(COL_4_INDECIES)

RIGHT_ORDER = []
RIGHT_ORDER.extend(COL_4_INDECIES)
RIGHT_ORDER.extend(COL_3_INDECIES)
RIGHT_ORDER.extend(COL_2_INDECIES)
RIGHT_ORDER.extend(COL_1_INDECIES)

STACK_OPTIONS = [1,1,1,1,2,2,2,2,3,3,3,3]

class Threes():
  def __init__(self, writeBeginning=False):
    self.board = Board()
    self.history = [
      {
        "state": self.board.serialState(),
        "reward": self.board.scoreBoard()
      }
    ]

    if writeBeginning != False:
      self.stdscr = curses.initscr()
      curses.cbreak()
      self.stdscr.keypad(1)
      self.writeBeginning = writeBeginning

  def __str__(self):
    return str(self.board)
    
  def env_start(self):
    self.board = Board()

    self.previousState = []
    self.currentState = self.board.serialState()
    self.counter = 0

    returnObs = Observation()
    returnObs.worldState = self.board.serialState()
    returnObs.availableActions = self.board.possibleMoves()

    return returnObs

  def env_step(self, action):
    self.previousState = self.board.serialState()
    self.executeMove(action.actionValue)

    self.counter += 1

    lastActionValue = action.actionValue
    observation = Observation()
    observation.worldState = self.board.serialState()
    observation.availableActions = self.board.possibleMoves()
    observation.isTerminal = not self.board.movesExists()

    rewardValue = self.calculateReward(lastActionValue)
    reward = Reward(rewardValue)

    return observation, reward

  def env_reset(self):
    self.env_start()

  def printOutput(self, direction):
    # Clear print space
    self.stdscr.addstr(self.writeBeginning,0,blankSpace())

    # Write board
    self.stdscr.addstr(self.writeBeginning,0,str(self.board))
    self.stdscr.addstr(self.writeBeginning+6,0,"Hit 'q' to quit")
    self.stdscr.addstr(self.writeBeginning+7, 0, direction)
    self.stdscr.addstr(self.writeBeginning+7,0,"")
    self.stdscr.refresh()

  def getInput(self):
    key = self.stdscr.getch()
    if key == curses.KEY_UP:
      direction = UP
    elif key == curses.KEY_DOWN:
      direction = DOWN
    elif key == curses.KEY_LEFT:
      direction = LEFT
    elif key == curses.KEY_RIGHT:
        direction = RIGHT
    else:
      direction = False

    return direction

  def executeMove(self, direction):
    if type(direction) == int:
      direction = ALL_MOVES[direction]

    # Quit on non move key
    if not direction:
      return False

    # Move board
    self.board.move(direction)

    # Track history
    self.history.append({
      "state": self.board.serialState(),
      "reward": self.board.scoreBoard()
    })

    # Check for game over
    if not self.board.movesExists():
      return False

    return True

  def calculateReward(self, lastAction=0):
    if len(self.history) < 2:
      return self.history[-1]["reward"]
    return self.history[-1]["reward"] - self.history[-2]["reward"]

  def play(self):
    direction = ""
    while True:
      # Print game and get input
      self.printOutput(direction)
      direction = self.getInput()

      if not self.executeMove(direction):
        break

    self.stdscr.addstr(self.writeBeginning+8, 0, "Game Over")
    curses.endwin()

class Board():
  def __init__(self):
    self.board = [
      [Tile(0),Tile(0),Tile(0),Tile(0)],
      [Tile(0),Tile(0),Tile(0),Tile(0)],
      [Tile(0),Tile(0),Tile(0),Tile(0)],
      [Tile(0),Tile(0),Tile(0),Tile(0)]
    ]
    self.generateIncomingStack()
    self.initalizeBoardValues()

    self.moveOptions = {
      UP: {
        "order": UP_ORDER,
        "front_check": self.getTileIdxAbove
      },
      RIGHT: {
        "order": RIGHT_ORDER,
        "front_check": self.getTileIdxRight
      },
      DOWN: {
        "order": DOWN_ORDER,
        "front_check": self.getTileIdxBelow
      },
      LEFT: {
        "order": LEFT_ORDER,
        "front_check": self.getTileIdxLeft
      }
    }

  def serialState(self):
    state = []
    for i in range(0,NUM_TILES):
      state.append(self[i].value)
    state.append(self.stack[-1])
    return state

  def initalizeBoardValues(self):
    initialVals = []
    availableSpots = UP_ORDER[:]

    # Generate initial values
    for i in range(0,9):
      initialVals.append(self.getIncoming())

    # Pick spots for all initial vals
    for val in initialVals:
      tileIdx = random.choice(availableSpots)
      availableSpots.remove(tileIdx)
      self[tileIdx].value = val

  # Choose an incoming number
  def getIncoming(self):
    val = self.stack.pop()
    if self.stack == []:
      self.generateIncomingStack()
    return val

  def generateIncomingStack(self):
    # Create stack of 4 1s, 2s, and 3s
    stackOptions = STACK_OPTIONS[:]

    # Insert a big card
    largestVal = self.getLargestVal()
    if largestVal >= 48:
      insertBig = random.randint(0,1)
      if insertBig:
        stackOptions.append(largestVal/8)

    random.shuffle(stackOptions)
    self.stack = stackOptions

  def __getitem__(self, key):
    if key == None:
      return None
    else:
      row = int(key/NUM_ROWS)
      col = key % NUM_COLS
      return self.board[row][col]

  def __str__(self):
    largestVal = self.getLargestVal()
    maxNumDigits = len(str(largestVal))

    returnStr = ""
    for row in self.board:
      for tile in row:
        returnStr += str(tile) + " " * (maxNumDigits-len(str(tile))) + " "
      returnStr += "\n"
    returnStr += "Incoming: " + str(self.stack[-1]) + "\n"
    returnStr += "Score: " + str(self.scoreBoard())

    return returnStr

  def move(self, direction):
    order = self.moveOptions[direction]["order"]
    nextTileMethod = self.moveOptions[direction]["front_check"]

    if not self.canMove(direction):
      return "Can't move"

    # Move tiles
    for tileIdx in order:
      tile = self[tileIdx]
      nextTileIdx = nextTileMethod(tileIdx)
      if nextTileIdx != None:
        if tile.canMove(self[nextTileIdx]):
          self[nextTileIdx].set(tile.value+self[nextTileIdx].value)
          self[tileIdx].set(0)

    # Bring in new tile
    lastRow = order[-4:]
    availableSpots = []
    for tileIdx in lastRow:
      if self[tileIdx].value == 0:
        availableSpots.append(tileIdx)
    incomingSpot = random.choice(availableSpots)
    self[incomingSpot].value = self.getIncoming()

    return "Success"

  def movesExists(self):
    return self.canMove(UP) or self.canMove(RIGHT) or self.canMove(DOWN) or self.canMove(LEFT)

  def canMove(self, direction):
    moveMatrix = self.moveMatrix(self.moveOptions[direction]["front_check"])

    if direction == UP or direction == DOWN:
      return self.sat(COLS, moveMatrix)
    else:
      return self.sat(ROWS, moveMatrix)

  def canMoveAV(self, direction):
    return self.canMove(ALL_MOVES[int(direction)])

  def moveMatrix(self, adjacentFunc):
    boolVals = []
    for tileIdx in range(0,NUM_TILES):
      if self[tileIdx].canMove(self[adjacentFunc(tileIdx)]):
        boolVals.append(True)
      else:
        boolVals.append(False)

    return boolVals

  def sat(self, sections, matrix):
    for section in sections:
      if matrix[section[0]] or matrix[section[1]] or matrix[section[2]] or matrix[section[3]]:
        return True
    return False

  def getTileInFront(self, idx, invalidTiles, offset):
    if idx in invalidTiles:
      return None
    else:
      return idx+offset

  def getTileIdxAbove(self, idx):
    return self.getTileInFront(idx, ROW_1_INDECIES, -NUM_COLS)

  def getTileIdxRight(self, idx):
    return self.getTileInFront(idx, COL_4_INDECIES, 1)

  def getTileIdxBelow(self, idx):
    return self.getTileInFront(idx, ROW_4_INDECIES, NUM_COLS)

  def getTileIdxLeft(self, idx):
    return self.getTileInFront(idx, COL_1_INDECIES, -1)

  def getLargestVal(self):
    largestVal = -1
    for i in range(0, NUM_TILES):
      if self[i].value > largestVal:
        largestVal = self[i].value
    return largestVal

  def scoreBoard(self):
    score = 0
    for tileIdx in range(0,NUM_TILES):
      if self[tileIdx].value != 1 and self[tileIdx].value != 2 and not self[tileIdx].empty():
        score += pow(3,(log(self[tileIdx].value/3,2)+1))
    return int(score)

  def possibleMoves(self):
    moves = []
    for i, move in enumerate(ALL_MOVES):
      if self.canMove(move):
        moves.append(i)
    return moves

class Tile():
  def __init__(self, value=0):
    self.value = value

  def __str__(self):
    return str(self.value)

  def empty(self):
    return self.value == 0

  def set(self, newValue):
    self.value = newValue

  def canCombineWith(self, otherTile):
    if otherTile.empty() and self.empty():
      return False
    if otherTile.empty() and not self.empty():
      return True
    if self.value == otherTile.value and (self.value != 1) and (self.value != 2):
      return True
    if self.value == 1 and otherTile.value == 2:
      return True
    if self.value == 2 and otherTile.value == 1:
      return True
    return False

  def canMove(self, tileInFront):
    if tileInFront == None:
      return False
    elif (self.canCombineWith(tileInFront)):
      return True
    return False

def blankSpace():
  blankSpaces = ""
  for i in range(0,10):
    for j in range(0,20):
      blankSpaces += " "
    blankSpaces += "\n"
  return blankSpaces

def main():
  writeBeginning = 0

  continuePlaying = True
  while continuePlaying:
    game = Threes(writeBeginning)
    game.play()
    writeBeginning += 10
  print

if __name__ == "__main__":
  main()
