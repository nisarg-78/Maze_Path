import time
from cv2 import FlannBasedMatcher
import pygame
pygame.init()

#colors
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLUE_2 = (29,53,87)
GREEN_2 = (42,157,143)
WHITE = (255,255,255)
GREY = (128,128,128)
GOLD = (255, 215, 0)

WIDHT = 600
GAP = 100
ROWS = WIDHT//GAP

WIN = pygame.display.set_mode((WIDHT, WIDHT))
pygame.display.set_caption("Maze Path")
WIN.fill((38,70,83))
clock = pygame.time.Clock()


class Spot:
    
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = row * GAP
        self.y = col * GAP
        self.color = BLUE_2
        self.neighbors = []
    

    def __repr__(self):
        return (f"{self.row},{self.col}")
    

    def draw(self, win, color=None):
        if not color:
            color = GREEN_2
        pygame.draw.rect(win, color, (self.x, self.y, GAP, GAP))
    

def make_spots():
    grid = []
    for i in range(ROWS):
        grid.append([])
        for j in range(ROWS):
            spot = Spot(i, j)
            grid[i].append(spot)
    return grid

    
def draw_grid_lines():
    for i in range(WIDHT//GAP):
        pygame.draw.line(WIN, WHITE, (0,i*GAP), (WIDHT ,i*GAP))
        pygame.draw.line(WIN, WHITE, (i*GAP, 0), (i*GAP, WIDHT))


def place_spots(win, spot_grid):

	for row in spot_grid:
		for spot in row:
			spot.draw(win)

	pygame.display.update()

    
spot_grid = make_spots()
place_spots(WIN, spot_grid)
draw_grid_lines()


maze = [[1 for _ in range(ROWS)] for _ in range(ROWS)]
def clear_maze():
    maze = [[1 for _ in range(ROWS)] for _ in range(ROWS)]

def path_finder(maze):

    for i in maze:
        print(i)
    # time.sleep(10)

    visited = [[0 for _ in range(len(maze[0]))] for _ in range(len(maze))]
    n = len(maze)
    m = len(maze[0])
    i = j = 0
    paths = []

    def solve_maze(maze, n, m, visited, i, j, moves):     # D L R U 

        pygame.display.update()
        time.sleep(0.05)
        print(i,j)
        
        if(i==n-1 and j==m-1):
            print(moves)
            paths.append(moves)
            spot_grid[j][i].draw(WIN, GOLD)
            time.sleep(1)

            # for row in spot_grid:
            #     for spot in row:
            #         spot.draw(WIN, GREEN_2)
            draw_grid_lines()
            return
            
        #Down
        if((i+1)<n and maze[i+1][j] and not visited[i+1][j]):
            visited[i][j] = 1
            spot_grid[j][i].draw(WIN, BLUE)
            draw_grid_lines()
            solve_maze(maze, n, m, visited, i+1, j, moves+'D')
            visited[i][j] = 0
            spot_grid[j][i].draw(WIN, GREEN_2)
            draw_grid_lines()
        #Left
        if((j-1)>=0 and maze[i][j-1] and not visited[i][j-1]):
            visited[i][j] = 1
            spot_grid[j][i].draw(WIN, BLUE)
            draw_grid_lines()
            solve_maze(maze, n, m, visited, i, j-1, moves+'L')
            visited[i][j] = 0
            spot_grid[j][i].draw(WIN, GREEN_2)
            draw_grid_lines()
        #Right
        if((j+1)<m and maze[i][j+1] and not visited[i][j+1]):
            visited[i][j] = 1
            spot_grid[j][i].draw(WIN, BLUE)
            draw_grid_lines()
            solve_maze(maze, n, m, visited, i, j+1, moves+'R')
            visited[i][j] = 0
            spot_grid[j][i].draw(WIN, GREEN_2)
            draw_grid_lines()
        #Up
        if((i-1)>=0 and maze[i-1][j] and not visited[i-1][j]):
            visited[i][j] = 1
            spot_grid[j][i].draw(WIN, BLUE)
            draw_grid_lines()
            solve_maze(maze, n, m, visited, i-1, j, moves+'U')
            visited[i][j] = 0
            spot_grid[j][i].draw(WIN, GREEN_2)
            draw_grid_lines()

    moves = ''
    solve_maze(maze, n, m, visited, i, j, moves)

    return paths


for row in spot_grid:
    for spot in row:
        print(spot, end=' ')
    print()


# window loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            col, row = pos[0]//GAP, pos[1]//GAP
            spot_grid[col][row].draw(WIN, GREY)
            maze[row][col] = 0
            print(maze[row])
        

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Space")
                path_finder(maze)
                for i in maze:
                    print(i)
            if event.key == pygame.K_r:
                print("R")
                clear_maze()
                place_spots(WIN, spot_grid)
                draw_grid_lines()

        
    pygame.display.update()
    clock.tick(60)
