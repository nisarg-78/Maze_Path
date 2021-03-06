import time, sys
from presets import preset_maze
import pygame
import concurrent.futures as cf

global_thread = cf.ThreadPoolExecutor(max_workers=1)

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

WIDHT = 800
GAP = 20
ROWS = WIDHT//GAP
delay = 0.05

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


def set_preset(num):
    maze = preset_maze[num]
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if not maze[i][j]:
                spot_grid[j][i].draw(WIN, GREY)
                pygame.display.update()
    return maze


def clear_maze():
    maze = [[1 for _ in range(ROWS)] for _ in range(ROWS)]
    return maze


def path_finder(maze):

    print("inside path_finder")

    visited = [[0 for _ in range(len(maze[0]))] for _ in range(len(maze))]
    n = len(maze)
    m = len(maze[0])
    i = j = 0
    paths = []

    def solve_maze(maze, n, m, visited, i, j, moves):

        pygame.display.update()
        time.sleep(delay)
        # print(i,j)
        
        if(i==n-1 and j==m-1):
            paths.append(moves)
            spot_grid[j][i].draw(WIN, GOLD)

            draw_grid_lines()
            pygame.display.update()
            time.sleep(3*delay)
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
        #Right
        if((j+1)<m and maze[i][j+1] and not visited[i][j+1]):
            visited[i][j] = 1
            spot_grid[j][i].draw(WIN, BLUE)
            draw_grid_lines()
            solve_maze(maze, n, m, visited, i, j+1, moves+'R')
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


def animate_shortest_path(future):

    i = j = 0
    path = future.result()
    path.sort(key=len)
    s_path = path[0]

    for move in s_path:
        time.sleep(0.01)
        if move == 'D':
            spot_grid[j][i].draw(WIN, GREEN)
            pygame.display.update()
            draw_grid_lines()
            i += 1
        elif move == 'L':
            spot_grid[j][i].draw(WIN, GREEN)
            pygame.display.update()
            draw_grid_lines()
            j -= 1
        elif move == 'R':
            spot_grid[j][i].draw(WIN, GREEN)
            pygame.display.update()
            draw_grid_lines()
            j += 1
        elif move == 'U':
            spot_grid[j][i].draw(WIN, GREEN)
            pygame.display.update()
            draw_grid_lines()
            i -= 1



# window loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
               
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            col, row = pos[0]//GAP, pos[1]//GAP
            spot_grid[col][row].draw(WIN, GREY)
            draw_grid_lines()
            maze[row][col] = 0

        if pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            col, row = pos[0]//GAP, pos[1]//GAP
            spot_grid[col][row].draw(WIN, GREEN_2)
            draw_grid_lines()
            maze[row][col] = 1
        
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                print("Space")
                global_thread.submit(path_finder, maze).add_done_callback(animate_shortest_path)
                
            if event.key == pygame.K_p:
                print("Maze: ")
                for row in maze:
                    print(row)

            if event.key == pygame.K_1:
                if len(preset_maze[0]) == ROWS:
                    maze = clear_maze()
                    place_spots(WIN, spot_grid)
                    draw_grid_lines()                
                    maze = set_preset(0)
                    draw_grid_lines()

            if event.key == pygame.K_2:
                if len(preset_maze[1]) == ROWS:
                    maze = clear_maze()
                    place_spots(WIN, spot_grid)
                    draw_grid_lines()
                    maze = set_preset(1)
                    draw_grid_lines()

            if event.key == pygame.K_UP:
                delay /= 2
                print(f"Delay: {delay}")

            if event.key == pygame.K_DOWN:
                delay *= 2
                print(f"Delay: {delay}")

            if event.key == pygame.K_r:
                print("R")
                maze = clear_maze()
                place_spots(WIN, spot_grid)
                draw_grid_lines()

        
    pygame.display.update()
    clock.tick(120)

pygame.quit()
sys.exit()
