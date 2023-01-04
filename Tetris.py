import pygame
from random import randint
pygame.init()

BLOCK_TYPES = [[(0, 0), (0, 1), (0, -1), (1, 0)],  # T
               [(0, 0), (0, 1), (0, 2), (0, -1)],  # I
               [(0, 0), (0, 1), (1, 1), (-1, 0)],  # S
               [(0, 0), (0, -1), (1, -1), (-1, 0)],  # Z
               [(0, 0), (0, 1), (1, 1), (1, 0)],  # O
               [(0, 0), (-1, 1), (-1, 0), (1, 0)],  # L
               [(0, 0), (1, 1), (-1, 0), (1, 0)],  # J
               ]

ROT_90_TRANS = [[0, 1],
                [-1, 0]]


# rotates a given 2D vector by 90 degrees a specified number of times
def rotate_vector(vec : tuple, iterations : int) -> tuple:
    while iterations < 0:
        iterations += 4

    for i in range(0, iterations):
        vec = (
                (ROT_90_TRANS[0][0] * vec[0]) + (ROT_90_TRANS[0][1] * vec[1]),
                (ROT_90_TRANS[1][0] * vec[0]) + (ROT_90_TRANS[1][1] * vec[1])
               )

    return vec


class Square:
    def __init__(self, s_x, s_y, grid, r, g, b):
        self.x = s_x
        self.y = s_y
        self.grid = grid
        self.r = r
        self.g = g
        self.b = b

    def moveDown(self):
        self.y += 1

    def draw(self):
        size = self.grid.square_size
        outer_square = pygame.Rect(20 + (self.x * size), 20 + (self.y * size), size, size)
        pygame.draw.rect(window, ((self.r + 20), (self.g + 20), (self.b + 20)), outer_square)


### --- Grid CLass --- ###

class Grid:
    """The background on which Tetris will be played. It
        will define the borders of the game."""
    def __init__(self,width,length,square_size):
        self.height = length
        self.width = width
        self.square_size = square_size
        self.grav_timer = 0
        self.outline = pygame.Rect(20,20,(self.square_size*self.width), (self.square_size*self.height))
        self.blocks = []

    def draw(self):
        pass

    def unpack_into_grid(self, tetra_block):
        for sq in tetra_block.get_squares():
            self.blocks.append(sq)

### --- Block Class --- ###
        
class Block:
    """A tetris block. There will be many of these
        on the screen at a time."""

    def __init__(self, grid,r,g,b, x, y):
        self.r = r
        self.g = g
        self.b = b
        self.x = x
        self.y = y
        self.grid = grid
        self.moving = True
        self.type = randint(0, 5)
        self.rotation = 0

        # push the block to the side until it is collision-free
        while not self.checkFullCollision(self.x, self.y + 3):
            if self.x < 4:
                self.x += 1
            else:
                self.x -= 1

    def moveSide(self, direction):
        if self.checkFullCollision(self.x + direction, self.y):
            self.x += direction

    def moveDown(self):
        if self.checkFullCollision(self.x, self.y + 1):
            self.y += 1
        else:
            self.moving = False

    def moveRotate(self, direction):
        self.rotation += direction

        # check validity
        if not self.checkFullCollision(self.x, self.y):
            self.rotation -= direction

    # returns False if moving this block to the specified position would cause an overlap
    def checkFullCollision(self, col_x, col_y):
        ret = True

        for b in BLOCK_TYPES[self.type]:
            sq_block = rotate_vector(b, self.rotation)
            ret = ret and self.checkCollisionSquare(col_x + sq_block[0], col_y + sq_block[1])

        return ret

    def checkCollisionSquare(self, col_x, col_y) -> bool:
        ret = True

        # check boundaries of the grid (excluding top)
        if col_y >= self.grid.height or col_x >= self.grid.width or col_x < 0:
            ret = False

        # check the squares in the grid
        for sq_block in self.grid.blocks:
            if sq_block.y == col_y and col_x == sq_block.x:
                ret = False

        return ret

    def drawSquare(self, x, y):
        size = self.grid.square_size
        outer_square = pygame.Rect(20 + (x * size), 20 + (y * size), size, size)
        pygame.draw.rect(window, ((self.r + 20), (self.g + 20), (self.b + 20)), outer_square)

    def draw(self):
        for b in BLOCK_TYPES[self.type]:
            sq_block = rotate_vector(b, self.rotation)
            self.drawSquare(self.x + sq_block[0], self.y + sq_block[1])

    def get_squares(self):
        squares = []

        for b in BLOCK_TYPES[self.type]:
            block_pos = rotate_vector(b, self.rotation)
            squares.append(Square(self.x + block_pos[0], self.y + block_pos[1], self.grid, self.r, self.g, self.b))

        return squares



### ---- MUSIC MIXTAPE (FIRE) ---- ###
# pygame.mixer.music.load("tetris_piano.wav")
# pygame.mixer.music.play(-1)


### ---- GLOBAL VARIABLES ---- ###
window = pygame.display.set_mode([750,650])
c = pygame.time.Clock()

BG = Grid(12,20,30) #12x30 grid of 30x30pxl squares
moving_block = Block(BG, randint(0,235), randint(0,235), randint(0,235), randint(0,BG.width-1), 1)

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
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            moving_block.moveRotate(1)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            moving_block.moveRotate(-1)
    
    window.fill((0,0,0))
    
    
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

    for square in BG.blocks:
        square.draw()
    moving_block.draw()

    if not moving_block.moving:
        BG.unpack_into_grid(moving_block)
        moving_block = Block(BG, randint(0,235), randint(0,235), randint(0,235), randint(0,BG.width-1), 1)

    pygame.draw.rect(window, (255, 255, 255), BG.outline, 5)

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
