import pygame
import random
import numpy as np
import copy

colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
    (180, 34, 143),
]

class Point:
    x=0
    y=0
    def __init__(self,x,y):
        self.x = x
        self.y = y
class Block:
        
    position = Point(0,0)
    rotationBlock = Point(0,0)
    shape = [Point(0,0),Point(0,0),Point(0,0),Point(0,0)]
    color = (0, 0, 0)
    def __init__(self, shape, rotationBlock, color):
        self.rotationBlock = rotationBlock
        self.shape = shape
        self.color = color
    def rotate(self):
        for i in range(len(self.shape)):
            a = self.shape[i].x -self.rotationBlock.x
            b = self.shape[i].y -self.rotationBlock.y
            self.shape[i].x = -b +self.rotationBlock.x
            self.shape[i].y = a + self.rotationBlock.y
    def getPositions(self):
        posArray = []
        for relPos in self.shape:
            x = relPos.x+self.position.x
            y = relPos.y+self.position.y
            posArray.append(Point(x,y))
            if x>9 or y>19:
                print(f"appending {x},{y}")
        return posArray
    

tBlock = Block([Point(0,0),Point(1,0),Point(2,0),Point(1,1)],Point(1,0),1)
iBlock = Block([Point(0,0),Point(1,0),Point(2,0),Point(3,0)],Point(1,0),2)
jBlock = Block([Point(0,0),Point(1,0),Point(2,0),Point(0,1)],Point(1,0),3)
lBlock = Block([Point(0,0),Point(1,0),Point(2,0),Point(2,1)],Point(1,0),4)
oBlock = Block([Point(0,0),Point(1,0),Point(0,1),Point(1,1)],Point(0,0),5)
sBlock = Block([Point(0,0),Point(1,0),Point(1,1),Point(2,1)],Point(1,0),6)
zBlock = Block([Point(0,1),Point(1,1),Point(1,0),Point(2,0)],Point(1,0),7)

blockArray = [tBlock, iBlock, jBlock, lBlock, oBlock, sBlock, zBlock]



class TetrisBoard:
    field = np.zeros(0)
    height = 0
    width = 0
    def __init__(self,height,width):
        self.height = height
        self.width = width
        self.fillBoard()
        
    def fillBoard(self):
        self.field = np.zeros(shape = [self.height,self.width])
        

class Tetris:
    state = "start"
    def __init__(self, height, width):
        self.level = 2
        self.score = 0
        self.state = "start"
        self.height = 0
        self.width = 0
        self.x = 100
        self.y = 60
        self.zoom = 20
        self.block = None
    
        self.height = height
        self.width = width
        self.board = TetrisBoard(height,width)
        self.score = 0
       

    def new_figure(self):
        self.block = blockArray[random.randint(0, 6)]
        self.block.position = Point(3,2)
    
    def intersects(self):
        for pos in self.block.getPositions():
            if(pos.x> self.width-1):
                return True
            if(pos.x<0):
                return True
            if(pos.y> self.height-1):
                return True
            if(self.board.field[pos.y][pos.x]>0):
                return True
        return False
    
    def blockIntersects(self,block):
        for pos in block.getPositions():
            if(pos.x> 9):
                return True
            if(pos.x<0):
                return True
            if(pos.y> 19):
                return True
            if(self.board.field[pos.y][pos.x]>0):
                return True
        return False
    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.board.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i in range(i, 1, -1):
                    for j in range(self.width):
                        self.board.field[i][j] = self.board.field[i - 1][j]
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.block.position.y += 1
        self.block.position.y -= 1
        self.freeze()

    def go_down(self):
        self.block.position.y += 1
        if self.intersects():
            self.block.position.y -= 1
            self.freeze()

    def freeze(self):
        for pos in self.block.getPositions():
            self.board.field[pos.y][pos.x] = self.block.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.block.position.x
        self.block.position.x += dx
        if self.intersects():
            self.block.position.x = old_x

    def rotate(self):
        old_block = self.block
        self.block.rotate()
        if self.intersects():
            self.block = old_block


class UserTetrisGame:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    size = (400, 500)
    game = Tetris(20, 10)
    pressing_down = False
    quitting = False
    fps = 25
    screen = pygame.display.set_mode(size)
    
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont('Calibri', 25, True, False)
        self.font1 = pygame.font.SysFont('Calibri', 65, True, False)
        self.text_game_over = self.font1.render("Game Over\n", True, (255, 125, 0))
        self.text_game_over1 = self.font1.render("Press ESC", True, (255, 215, 0))
        
    def userInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quitting = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.game.rotate()
                if event.key == pygame.K_DOWN:
                    self.pressing_down = True
                if event.key == pygame.K_LEFT:
                    self.game.go_side(-1)
                if event.key == pygame.K_RIGHT:
                    self.game.go_side(1)
                if event.key == pygame.K_SPACE:
                    self.game.go_space()
                if event.key == pygame.K_ESCAPE:
                    self.resetGame()

            if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.pressing_down = False
                        
    def drawBoard(self):
        for i in range(self.game.height):
                for j in range(self.game.width):
                    pygame.draw.rect(self.screen, self.GRAY, [self.game.x + self.game.zoom * j, self.game.y + self.game.zoom * i, self.game.zoom, self.game.zoom], 1)
                    if self.game.board.field[i][j] > 0:
                        pygame.draw.rect(self.screen, colors[int(self.game.board.field[i][j])],
                                        [self.game.x + self.game.zoom * j + 1, self.game.y + self.game.zoom * i + 1, self.game.zoom - 2, self.game.zoom - 1])
    def drawBoard(self):
        for i in range(self.game.height):
                for j in range(self.game.width):
                    pygame.draw.rect(self.screen, self.GRAY, [self.game.x + self.game.zoom * j, self.game.y + self.game.zoom * i, self.game.zoom, self.game.zoom], 1)
                    if self.game.board.field[i][j] > 0:
                        pygame.draw.rect(self.screen, colors[int(self.game.board.field[i][j])],
                                        [self.game.x + self.game.zoom * j + 1, self.game.y + self.game.zoom * i + 1, self.game.zoom - 2, self.game.zoom - 1])
    def drawPiece(self):
        if self.game.block is not None:
            for pos in self.game.block.getPositions():
                pygame.draw.rect(self.screen, colors[self.game.block.color],
                                        [self.game.x + self.game.zoom * pos.x + 1,
                                        self.game.y + self.game.zoom *pos.y + 1,
                                        self.game.zoom - 2, self.game.zoom - 2])
    def renderText(self):
        self.text = self.font.render("Score: " + str(self.game.score), True, self.BLACK)
        self.screen.blit(self.text, [0, 0])
        
        if self.game.state == "gameover":
            self.screen.blit(self.text_game_over, [20, 200])
            self.screen.blit(self.text_game_over1, [25, 265])
            
    def resetGame(self):
        self.game = Tetris(20, 10)
        self.playTetris()
        
    def playTetris(self):
        # Initialize the game engine

        # Define some colors

        pygame.display.set_caption("Tetris")

        # Loop until the user clicks the close button.
        clock = pygame.time.Clock()
        
        
        counter = 0

        while not self.quitting:
            if self.game.block is None:
                self.game.new_figure()
            counter += 1
            if counter > 100000:
                counter = 0

            if counter % (self.fps // self.game.level // 2) == 0 or self.pressing_down:
                if self.game.state == "start":
                    self.game.go_down()

            
            self.userInput()
            self.screen.fill(self.WHITE)
            
            self.drawBoard()
            self.drawPiece()
            
            self.renderText()

            pygame.display.flip()
            clock.tick(self.fps)

        pygame.quit() 
        



class AITetrisGame:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    size = (400, 500)
    game = Tetris(20, 10)
    pressing_down = False
    quitting = False
    fps = 25
    screen = pygame.display.set_mode(size)
    
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont('Calibri', 25, True, False)
        self.font1 = pygame.font.SysFont('Calibri', 65, True, False)
        self.text_game_over = self.font1.render("Game Over\n", True, (255, 125, 0))
        self.text_game_over1 = self.font1.render("Press ESC", True, (255, 215, 0))
        
    def generateEndStates(self):
        blockEndStates = []
        #<--------------------------------------------------------------add rotations
        blockCopy = copy.copy(self.game.block)
        for i in range(0,4):
            blockCopy.rotate()
            for xPos in range(0,self.game.width-2):
                tempBlock = copy.copy(blockCopy)
                tempBlock.position = Point(xPos,0)
                if(self.game.blockIntersects(tempBlock)):
                    break
                while(not self.game.blockIntersects(tempBlock)):
                    tempBlock.position.y +=1
                tempBlock.position.y -= 1
                if(not self.game.blockIntersects(tempBlock)):
                    blockEndStates.append(tempBlock)
        return blockEndStates
    
    def moveToEndState(self, endStateX):
        if(self.game.block.position.x!=endStateX):
            if(self.game.block.position.x<endStateX):
                self.game.go_side(1)
            if(self.game.block.position.x>endStateX):
                self.game.go_side(-1)
        else:
            self.game.go_down()
    def drawBoard(self):
        for i in range(self.game.height):
                for j in range(self.game.width):
                    pygame.draw.rect(self.screen, self.GRAY, [self.game.x + self.game.zoom * j, self.game.y + self.game.zoom * i, self.game.zoom, self.game.zoom], 1)
                    if self.game.board.field[i][j] > 0:
                        pygame.draw.rect(self.screen, colors[int(self.game.board.field[i][j])],
                                        [self.game.x + self.game.zoom * j + 1, self.game.y + self.game.zoom * i + 1, self.game.zoom - 2, self.game.zoom - 1])
   
    def drawPiece(self):
        if self.game.block is not None:
            for pos in self.game.block.getPositions():
                pygame.draw.rect(self.screen, colors[self.game.block.color],
                                        [self.game.x + self.game.zoom * pos.x + 1,
                                        self.game.y + self.game.zoom *pos.y + 1,
                                        self.game.zoom - 2, self.game.zoom - 2])
    def renderText(self):
        self.text = self.font.render("Score: " + str(self.game.score), True, self.BLACK)
        self.screen.blit(self.text, [0, 0])
        
        if self.game.state == "gameover":
            self.screen.blit(self.text_game_over, [20, 200])
            self.screen.blit(self.text_game_over1, [25, 265])
            
    def resetGame(self):
        self.game = Tetris(20, 10)
        self.playTetris()
    
    def generateNumpyEndstateBoard(self,endstateBlock):
        endStateBoardCopy = copy.copy(self.game.board.field)
        for i in range(self.game.width-1):
            for j in range(self.game.height-1):
                if(endStateBoardCopy[j][i]>0):
                    endStateBoardCopy[j][i] = 1
        for pos in endstateBlock.getPositions():
            if(pos.y<20 and pos.y<10):
                endStateBoardCopy[pos.y][pos.x] = 1
        return endStateBoardCopy
    def playTetris(self,model):
        # Initialize the game engine

        # Define some colors

        pygame.display.set_caption("Tetris")

        # Loop until the user clicks the close button.
        clock = pygame.time.Clock()
        
        
        counter = 0

        while not self.quitting:
            if self.game.block is None:
                self.game.new_figure()
                endStates = self.generateEndStates()
            counter += 1
            if counter > 100000:
                counter = 0

            if counter % (self.fps // self.game.level // 2) == 0 or self.pressing_down:
                if self.game.state == "start":
                    self.game.go_down()

            
            
            endStateBoards = []
            for endStateBlock in endStates:
                print(endStateBlock.position.x)
                endStateBoards = np.append(endStateBoards,self.generateNumpyEndstateBoard(endStateBlock))
            endStateBoards = np.reshape(endStateBoards,[len(endStates),20,10])
            modelPredictions = model.predict(endStateBoards)
            for x in range(len(modelPredictions)):
                print(modelPredictions[x][0])
            
            self.moveToEndState(endStates[0].position.x)
                
            self.screen.fill(self.WHITE)
            
            self.drawBoard()
            self.drawPiece()
            
            self.renderText()

            pygame.display.flip()
            clock.tick(self.fps)

        pygame.quit() 
        