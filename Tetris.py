import pygame
from random import randint
pygame.init()


### --- Grid CLass --- ###

class Grid:
    """The background on which Tetris will be played. It
        will define the borders of the game."""
    def __init__(self,width,length,square_size):
        self.height = length
        self.width = width
        self.square_size = square_size
        self.grav_timer = 0
        self.outline = pygame.Rect(20,20,(self.square_size*self.width),(self.square_size*self.height))
        self.blocks = []
    def draw(self):
        pass









### --- Block Class --- ###
        
class Block:
    """A singular square. There will be many of these
        on the screen at a time."""
    def __init__(self, grid,r,g,b, x, y):
        self.r = r
        self.g = g
        self.b = b
        self.x = x
        self.y = y
        self.grid = grid
        self.moving = True
    def moveDown(self):
        willMove = True
        for square in self.grid.blocks:
            if square.y == self.y + 1 and self.x == square.x:
                 willMove = False
        if self.y == self.grid.height-1:
            willMove = False
        if willMove:
            self.y += 1
        else:
            self.moving = False
    def willMoveSide(self):
        pass
    def moveSide(self, direction):
        willMove = True
        for square in self.grid.blocks:
            if square.x == self.x + direction and square.y == self.y:
                willMove = False
        if self.x + direction == self.grid.width or self.x + direction == -1:
            willMove = False
        if willMove:
            self.x += direction
    def draw(self):
        x = self.x
        y = self.y
        size = self.grid.square_size
        outer_square = pygame.Rect(20+(x*size), 20+(y*size), size, size)
        inner_square = pygame.Rect(0,0, size*0.8, size*0.8)
        inner_square.x = outer_square.x + (0.1*size)
        inner_square.y = outer_square.y + (0.1*size)
        pygame.draw.rect(window, (self.r, self.g, self.b), outer_square)
        pygame.draw.rect(window, ((self.r + 20), (self.g + 20), (self.b + 20)), inner_square)





class TetraBlock:
    """A group of four blocks that will fall onto the screen."""
    def __init__(self, window):
        self.window = window
        self.r = randint(0,255)
        self.g = randint(0,255)
        self.b = randint(0,255)
        self.x = randint(1,self.window.width-5)

        block_types = [ [ (0,0), (0,1),  (0,-1),  (1,0)  ],  # T
                        [ (0,0), (0,1),  (0,2),   (0,-1) ],  # I
                        [ (0,0), (0,1),  (1,1),  (-1,0)  ],  # S
                        [ (0,0), (0,-1), (1,-1), (-1,0)  ],  # Z
                        [ (0,0), (0,1),  (1,1),   (1,0)  ],  # O
                        [ (0,0), (-1,1), (-1,0),  (1,0)  ],  # L
                        [ (0,0), (1,1),  (-1,0),  (1,0)  ],  # J
                        ]
        
        self.type = randint(0,6)
        self.pieces = []
        for x in range(0,4):
            X_pos, Y_pos = block_types[self.type][x]
            self.pieces.append(Block(self.grid, self.r, self.g, self.b, X_pos+self.x,Y_pos+2))
    def moveDown(self):

        movedown = True
        for piece in self.pieces:
            for block in BG:
                if block.x == piece.x-1:
                    movedown = False
        if movedown:
            for piece in self.pieces:
                pieces.moveDown
                

    def moveSide(self):
        moveside = True
        for piece in self.pieces:
            for block in BG.blocks:
                pass
    def draw(self):
        for piece in self.pieces:
            piece.draw()



### ---- MUSIC MIXTAPE (FIRE) ---- ###
pygame.mixer.music.load("tetris_piano.wav")
pygame.mixer.music.play(-1)


### ---- GLOBAL VARIABLES ---- ###
window = pygame.display.set_mode([750,650])
c = pygame.time.Clock()

BG = Grid(12,20,30) #12x30 grid of 30x30pxl squares
moving_block = Block(BG, randint(0,235), randint(0,235), randint(0,235), randint(0,BG.width-1), 0)

running = True

############# ------------- MAIN LOOP ------------- #############

while running:
    #Check arrow keys and quit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            moving_block.moveSide(1)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            moving_block.moveSide(-1)
    
    window.fill((170,170,170))
    
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_DOWN]:
        if BG.grav_timer > 100:
            BG.grav_timer = 0
            
            moving_block.moveDown()
    else:
        if BG.grav_timer > 500:
            BG.grav_timer = 0
            moving_block.moveDown()
        
            


    BG.grav_timer += c.get_time()
    moving_block.draw()
    if moving_block.moving == False:
        BG.blocks.append(moving_block)
        moving_block = Block(BG, randint(0,235), randint(0,235), randint(0,235), randint(0,BG.width-1), 0)
    for square in BG.blocks:
        square.draw()

    pygame.draw.rect(window, (0,0, 0), BG.outline, 5)
    ### --- REMOVING COMPLETED LAYERS --- ###
    for layer in range(0,BG.height):
        counter = 0
        removed = []
        for square in BG.blocks:
            if square.y == layer:
                counter += 1
                removed.append(square)
        if counter == BG.width:
            for square in removed:
                BG.blocks.remove(square)
            for x in range(1,BG.height+1):
                for square in BG.blocks:
                    if square.y == layer - x:
                        square.moveDown()
                
    pygame.display.flip()
    c.tick(30)

pygame.quit()
