import curses

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

class InlinePrinter():
  def __init__(self):
    self.stdscr = curses.initscr()
    curses.cbreak()

  def printLine(self, line, data):
    self.stdscr.addstr(line, 0, data)
    self.stdscr.refresh()
