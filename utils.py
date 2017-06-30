import curses
import datetime

def blankSpace():
  blankSpaces = ""
  for i in range(0,10):
    for j in range(0,20):
      blankSpaces += " "
    blankSpaces += "\n"
  return blankSpaces

def sat(sections, matrix):
  for section in sections:
    if matrix[section[0]] or matrix[section[1]] or matrix[section[2]] or matrix[section[3]]:
      return True
  return False

def calculateTileInFront(idx, invalidTiles, offset):
  if idx in invalidTiles:
    return None
  else:
    return idx+offset

def createTimeStampedFile(dir,ext="txt"):
  dateString = str(datetime.datetime.now().isoformat())
  dateString = dateString.replace("-","_")
  dateString = dateString.split(".")[0]
  dateString = dateString.replace(":",".")
  dateString = dateString.replace("T", "-")

  outputfile = open(dir + "/" + dateString + "." + ext, "w+")

  return outputfile

class Printer():
  def __init__(self, inlineMode):
    self.inlineMode = inlineMode

  def setInlineMode(self, inlineMode):
    self.inlineMode = inlineMode
    if self.inlineMode:
      self.stdscr = curses.initscr()
      curses.cbreak()

  def printLine(self, line, data):
    if self.inlineMode:
      self.stdscr.addstr(line, 0, data)
      self.stdscr.refresh()
    else:
      print(data)

  def getInput(self):
    if self.inlineMode:
      key = self.stdscr.getch()
    else:
      key = raw_input("Enter Move: ")
    return key

  def end(self):
    if self.inlineMode:
      curses.endwin()

printer = Printer(True)
