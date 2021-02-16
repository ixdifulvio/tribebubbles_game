import sys
from random import randint
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton

CELL_COUNT = 8
CELL_SIZE = 50
GRID_ORIGINX = 175
GRID_ORIGINY = 175
W_WIDTH = 850
W_HEIGHT = 750

class TribeBubbles(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tribe Bubbles')
        self.setGeometry(300, 300, W_WIDTH, W_HEIGHT)
        self.__points = 0
        self.__multiplier = 1
        self.__win = False
        self.__readyToExplode = False
        self.__hasExploded = True
        self.__turn = 0
        self.__randcolor = QColor(randint(0,255), randint(0,255), randint(0,255))
        self.__grid = [['', '', '', '', '', '', '', ''], ['', '', '', '', '', '', '', ''], ['', '', '', '', '','', '', ''], ['', '', '', '', '','', '', ''], ['', '', '', '', '','', '', ''], ['', '', '', '', '','', '', ''], ['', '', '', '', '','', '', ''], ['', '', '', '', '','', '', '']]
        self.__used = [['F', 'F', 'F', 'F', 'F', 'F', 'F', 'F'], ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'F'], ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'F'], ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'F'], ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'F'], ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'F'], ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'F'], ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'F']]
        self.show()
        
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        # draws grid
        for r in range(CELL_COUNT):
            for c in range(CELL_COUNT):
                qp.setPen(QPen(Qt.black, 1))
                qp.drawRect(GRID_ORIGINX + c*CELL_SIZE, GRID_ORIGINY + r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                #draws a circle if it is marked
                if self.__grid[r][c] == 0:
                    qp.drawEllipse(GRID_ORIGINX + c*CELL_SIZE, GRID_ORIGINY + r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        #draws blocker        
        for r in range(CELL_COUNT):
            for c in range(CELL_COUNT):
                if self.__grid[r][c] == 1:
                    qp.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
                    qp.drawRect(GRID_ORIGINX + c*CELL_SIZE, GRID_ORIGINY + r*CELL_SIZE, CELL_SIZE, CELL_SIZE) 
         # draws number of points and multiplier
        qp.drawText(GRID_ORIGINX, GRID_ORIGINY + 420, "Points: " + str(self.__points) + ' * ' + str(self.__multiplier))
        # draws game over once the grid is filled
        qp.setPen(QPen(Qt.red, 3))
        if self.__win == True or self.gameover() == True:
            qp.drawText(GRID_ORIGINX + 150, GRID_ORIGINY - 30, "Game over!")
        # draws button for explode
        qp.fillRect(625, 225, 50, 50, self.__randcolor)
        # label for explode button
        qp.setPen(QPen(Qt.black, 3))
        qp.drawText(625, 200, "Explode button")
        if self.canExplode() == False:
            qp.drawText(625, 300, "Explode is not ready yet!")
            qp.drawText(625, 320, "You need " + str(30 - (self.__turn % 30)) + " more turns!")
        else:
            qp.drawText(625, 300, "Press to explode!")
        qp.end()
        
    def dissapear(self):
        #checks horizontal
        mylist = []
        line = 0
        for n in range(8): 
            for i in range(5):
                if self.__grid[n][i] == self.__grid[n][i+1] == self.__grid[n][i+2] == self.__grid[n][i+3] == 0:
                    if self.__used[n][i] == self.__used[n][i+1] == self.__used[n][i+2] == self.__used[n][i+3] == 'F':
                        line += 1 
                    for c in range(i, i + 4):
                        self.__used[n][c] = 'T'
                    mylist.append((n,i))
                    mylist.append((n,i+1))
                    mylist.append((n,i+2))
                    mylist.append((n,i+3))
                    if i + 4 < 8 and self.__grid[n][i+4] == 0:
                        mylist.append((n,i+4))
                    if i + 5 < 8 and self.__grid[n][i+5] == 0:
                        mylist.append((n,i+5))
                    if i + 6 < 8 and self.__grid[n][i+6] == 0:
                        mylist.append((n,i+6))
                    if i + 7 < 8 and self.__grid[n][i+7] == 0:
                        mylist.append((n,i+7)) 
                        
        #resets used after checking each type of combo
        for i in range(8):
            for j in range(8):
                self.__used[i][j] = 'F'
                                         
        #checks vertical
        for i in range(8): 
            for n in range(5):
                if self.__grid[n][i] == self.__grid[n+1][i] == self.__grid[n+2][i] == self.__grid[n+3][i] == 0:
                    if self.__used[n][i] == self.__used[n+1][i] == self.__used[n+2][i] == self.__used[n+3][i] == 'F':
                        line += 1
                    for r in range(n, n + 4):
                        self.__used[r][i] = 'T'
                    mylist.append((n,i))
                    mylist.append((n+1, i))
                    mylist.append((n+2, i))
                    mylist.append((n+3, i))
                    if n + 4 < 8 and self.__grid[n+4][i] == 0:
                        mylist.append((n+4, i))
                    if n + 5 < 8 and self.__grid[n+5][i] == 0:
                        mylist.append((n+5, i))    
                    if n + 6 < 8 and self.__grid[n+6][i] == 0:
                        mylist.append((n+6, i))    
                    if n + 7 < 8 and self.__grid[n+7][i] == 0:
                        mylist.append((n+7, i))
        
        #resets used after checking each type of combo
        for i in range(8):
            for j in range(8):
                self.__used[i][j] = 'F'
                
        #diagonal (down to the right)
        for i in range(5):
            for j in range(5):
                if self.__grid[i][j] == self.__grid[i+1][j+1] == self.__grid[i+2][j+2]  == self.__grid[i+3][j+3] == 0:
                    if self.__used[i][j] == self.__used[i+1][j+1] == self.__used[i+2][j+2]  == self.__used[i+3][j+3] == 'F':
                        line += 1
                        self.__used[i][j] = 'T'
                        self.__used[i+1][j+1] = 'T'
                        self.__used[i+2][j+2]  = 'T'
                        self.__used[i+3][j+3] = 'T'
                    mylist.append((i,j))
                    mylist.append((i+1, j+1))
                    mylist.append((i+2, j+2))
                    mylist.append((i+3, j+3))
                    if i + 4 < 8 and j + 4 < 8 and self.__grid[i+4][j+4] == 0:
                        mylist.append((i+4, j+4))
                    if i + 5 < 8 and j + 5 < 8 and self.__grid[i+5][j+5] == 0:
                        mylist.append((i+5, j+5))
                    if i + 6 < 8 and j + 6 < 8 and self.__grid[i+6][j+6] == 0:
                        mylist.append((i+6, j+6))
                    if i + 7 < 8 and j + 7 < 8 and self.__grid[i+7][j+7] == 0:
                        mylist.append((i+7, j+7))
                        
        #reset used            
        for i in range(8):
            for j in range(8):
                self.__used[i][j] = 'F'            
                        
        #diagonal (down to the left)
        for i in range(0,5):
            for j in range(3,8):
                if self.__grid[i][j] == self.__grid[i+1][j-1] == self.__grid[i+2][j-2] == self.__grid[i+3][j-3] == 0:
                    if self.__used[i][j] == self.__used[i+1][j-1] == self.__used[i+2][j-2] == self.__used[i+3][j-3] == 'F':
                        line += 1
                        self.__used[i][j] = 'T'
                        self.__used[i+1][j-1] = 'T'
                        self.__used[i+2][j-2] = 'T'
                        self.__used[i+3][j-3] = 'T'
                    mylist.append((i,j))
                    mylist.append((i+1,j-1))
                    mylist.append((i+2,j-2))    
                    mylist.append((i+3,j-3))
                    if i + 4 < 8 and j- 4 >= 0 and self.__grid[i+4][j-4] == 0:
                        mylist.append((i+4, j-4))
                    if i + 5 < 8 and j - 5 >= 0 and self.__grid[i+5][j-5] == 0:
                        mylist.append((i+5, j-5))
                    if i + 6 < 8 and j - 6 >= 0 and self.__grid[i+6][j-6] == 0:
                        mylist.append((i+6, j-6))
                    if i + 7 < 8 and j - 7 >= 0 and self.__grid[i+7][j-7] == 0:
                        mylist.append((i+7, j-7))
                 
        #eliminates repeats and replaces all the consecutive bubbles with empty spaces
        mylist = list(set(mylist))
        for i,j in mylist:
            self.__grid[i][j] = ''
        #sets multiplier
        if line <= 1:
            self.__multiplier = 1
        else:
            self.__multiplier = line
        #calculates total points
        self.__points += len(mylist) * self.__multiplier
    
        #resets used
        for i in range(8):
            for j in range(8):
                self.__used[i][j] = 'F'
                
    def gameover(self):
        #game over is true if every single index is occupied by a 0 or 1
        for r in range(8):
            for c in range(8):
                if self.__grid[r][c] == '':
                    self.__win = False
                    return self.__win
        self.__win = True
        return self.__win
    
    def canExplode(self):
        #Explode button can be used after 30 turns 
        if self.__turn % 30 == 0 and self.__turn != 0:
            self.__hasExploded = False
        if self.__hasExploded == False:
            return True
        else:
            return False 
    
    def explode(self):
        # executes explode
        self.__hasExploded = True
        explodex = randint(0, 4)
        explodey = randint(0, 4)
        for r in range(explodey, explodey + 4):
            for c in range(explodex, explodex + 4):
                self.__grid[r][c] = ''
        self.__turn = 0
        
    def mousePressEvent(self, event):
        #stops the game if the grid is full
        if self.gameover() == True:
            return
        
        # figure out which cell the click is in
        row = (event.y() - GRID_ORIGINY) // CELL_SIZE
        col = (event.x() - GRID_ORIGINX) // CELL_SIZE
        
        #explode button
        if row == 1 and col == 9:
            if self.canExplode() == True:
                self.explode()
                
        #print(str(row) + ", " + str(col))
        
        #marking 0 or 1
        if 0 <= row < CELL_COUNT and 0 <= col < CELL_COUNT:
            # if the grid is not marked
            if self.__grid[row][col] == '':
                self.__turn += 1
                self.__grid[row][col] = 0
                self.dissapear()
                randomx = randint(0,7)
                randomy = randint(0,7)
                self.__grid[randomy][randomx] = 1
                
        self.update()
        
    
        
        
if __name__ == '__main__':
  app = QApplication(sys.argv)
  ex = TribeBubbles()
  sys.exit(app.exec_())

