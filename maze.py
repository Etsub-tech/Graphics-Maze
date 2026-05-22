import pygame
import random
import sys
import time

R = 15          # rows
C = 20          # columns
CELL = 36       # pixels per cell

# Colours
WHITE      = (245, 243, 238)
BLACK      = (30,  28,  26)
WALL_COL   = (30,  28,  26)
VISITED_BG = (214, 237, 249)   # light blue, the generator
MOUSE_COL  = (55,  138, 221)   # blue dot, position of the current mouse
DEAD_END   = (240, 149, 123)   # coral indicates dead end
SOLUTION   = (150, 196,  89)   # green, final solution path
START_COL  = (239, 159,  39)   # amber, start of the cell
END_COL    = (239, 159,  39)   # amber, end cell
GRID_BG    = (245, 243, 238)

GEN_DELAY  = 15
SOLVE_DELAY = 30
BONUS_MODE = True

northWall = [[1] * C for _ in range(R + 1)]
eastWall  = [[1] * (C + 1) for _ in range(R)]

gen_visited = [[False] * C for _ in range(R)]


def reset_walls():
    global northWall, eastWall, gen_visited
    northWall   = [[1] * C for _ in range(R + 1)]
    eastWall    = [[1] * (C + 1) for _ in range(R)]
    gen_visited = [[False] * C for _ in range(R)]


def cell_rect(r, c):
    return (c * CELL, r * CELL, CELL, CELL)


def draw_cell_bg(surface, r, c, colour):
    pygame.draw.rect(surface, colour, cell_rect(r, c))


def draw_walls(surface):
    
    W = C * CELL
    H = R * CELL

    for r in range(R):
        for c in range(C):
            x, y = c * CELL, r * CELL

            # North wall
            if northWall[r][c]:
                pygame.draw.line(surface, WALL_COL, (x, y), (x + CELL, y), 2)
            
            # East wall
            if eastWall[r][c + 1]:
                pygame.draw.line(surface, WALL_COL,
                                 (x + CELL, y), (x + CELL, y + CELL), 2)


    for c in range(C):
        if northWall[R][c]:
            x = c * CELL
            pygame.draw.line(surface, WALL_COL, (x, H), (x + CELL, H), 2)

    # Left border: eastWall[r][0] is the wall on the LEFT of column 0
    for r in range(R):
        if eastWall[r][0]:
            y = r * CELL
            pygame.draw.line(surface, WALL_COL, (0, y), (0, y + CELL), 2)


def draw_dot(surface, r, c, colour, radius_frac=0.28):
    cx = c * CELL + CELL // 2
    cy = r * CELL + CELL // 2
    pygame.draw.circle(surface, colour, (cx, cy), int(CELL * radius_frac))


##generating the maze
def unvisited_neighbours(r, c):
    """Return list of (nr, nc, direction) for unvisited neighbours."""
    result = []
    if r > 0   and not gen_visited[r - 1][c]: result.append((r-1, c, 'N'))
    if r < R-1 and not gen_visited[r + 1][c]: result.append((r+1, c, 'S'))
    if c > 0   and not gen_visited[r][c - 1]: result.append((r, c-1, 'W'))
    if c < C-1 and not gen_visited[r][c + 1]: result.append((r, c+1, 'E'))
    return result


def remove_wall(r, c, direction):
    if direction == 'N': northWall[r][c]     = 0
    elif direction == 'S': northWall[r+1][c] = 0
    elif direction == 'W': eastWall[r][c]    = 0
    elif direction == 'E': eastWall[r][c+1]  = 0


def generate_maze_animated(surface, clock, start_row, end_row):
    reset_walls()

    
    eastWall[start_row][0] = 0
    eastWall[end_row][C]   = 0

    # the mouse starts at a random cell
    sr, sc = random.randrange(R), random.randrange(C)
    gen_visited[sr][sc] = True
    stack = [(sr, sc)]

    while stack:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        r, c = stack[-1]
        neighbours = unvisited_neighbours(r, c)

        if neighbours:

            # it chooses a random unvisited neighbour
            nr, nc, direction = random.choice(neighbours)

            # it removes the wall toward the chosen neighbour
            remove_wall(r, c, direction)

            # for the bonus part
            if BONUS_MODE and random.random() < 0.05:

                possible = []

                if r > 0:
                    possible.append('N')
                if r < R - 1:
                    possible.append('S')
                if c > 0:
                    possible.append('W')
                if c < C - 1:
                    possible.append('E')

                if possible:
                    bonus_dir = random.choice(possible)
                    remove_wall(r, c, bonus_dir)

            # continue DFS
            gen_visited[nr][nc] = True
            stack.append((nr, nc))

        else:
            #backtracks for the dead end 
            stack.pop()


        
        surface.fill(GRID_BG)
        # Shade visited cells
        for row in range(R):
            for col in range(C):
                if gen_visited[row][col]:
                    draw_cell_bg(surface, row, col, VISITED_BG)
        # Highlight current mouse position
        if stack:
            cr, cc = stack[-1]
            draw_cell_bg(surface, cr, cc, MOUSE_COL)
            draw_dot(surface, cr, cc, WHITE)

        draw_walls(surface)
        pygame.display.flip()
        clock.tick(1000 // GEN_DELAY)


# maze solver
def can_move(r, c, direction):
    
    if direction == 'N': return r > 0   and northWall[r][c]     == 0
    if direction == 'S': return r < R-1 and northWall[r+1][c]   == 0
    if direction == 'W': return c > 0   and eastWall[r][c]       == 0
    if direction == 'E': return c < C-1 and eastWall[r][c+1]     == 0
    return False


def solve_maze_animated(surface, clock, start_row, end_row):
    # cell_state: 0 means unvisited, 1 means on stack (active), 2 means dead end
    cell_state = [[0] * C for _ in range(R)]
    parent     = [[None] * C for _ in range(R)]   

    # Start at top left, end at bottom right
    start = (start_row, 0)
    end = (end_row, C-1)

    stack = [start]
    cell_state[start_row][0] = 1

    DIRS = ['N', 'S', 'W', 'E']

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        r, c = stack[-1]

        #Goal reached 
        if (r, c) == end:
            # Reconstruct path
            path = []
            cur = end
            while cur is not None:
                path.append(cur)
                cur = parent[cur[0]][cur[1]]
            path.reverse()

            # Draw solution
            surface.fill(GRID_BG)
            for row in range(R):
                for col in range(C):
                    if cell_state[row][col] == 2:
                        draw_cell_bg(surface, row, col, DEAD_END)
            for (pr, pc) in path:
                draw_cell_bg(surface, pr, pc, SOLUTION)
            draw_walls(surface)
            draw_dot(surface, start[0], start[1], START_COL)
            draw_dot(surface, end[0],   end[1],   END_COL)
            pygame.display.flip()
            return path

        #trying a random direction to move
        random.shuffle(DIRS)
        moved = False
        for d in DIRS:
            if can_move(r, c, d):
                nr, nc = (r-1,c) if d=='N' else (r+1,c) if d=='S' else \
                         (r,c-1) if d=='W' else (r,c+1)
                if cell_state[nr][nc] == 0:
                    cell_state[nr][nc] = 1
                    parent[nr][nc] = (r, c)
                    stack.append((nr, nc))
                    moved = True
                    break

        if not moved:
            # Dead end: mark and backtrack
            cell_state[r][c] = 2
            stack.pop()

        surface.fill(GRID_BG)
        for row in range(R):
            for col in range(C):
                if cell_state[row][col] == 1:
                    draw_cell_bg(surface, row, col, VISITED_BG)
                elif cell_state[row][col] == 2:
                    draw_cell_bg(surface, row, col, DEAD_END)
        if stack:
            cr, cc = stack[-1]
            draw_dot(surface, cr, cc, MOUSE_COL)
        draw_walls(surface)
        draw_dot(surface, start[0], start[1], START_COL)
        draw_dot(surface, end[0],   end[1],   END_COL)
        pygame.display.flip()
        clock.tick(1000 // SOLVE_DELAY)

    return None   # no path found


#  main
def main():
    pygame.init()
    width  = C * CELL
    height = R * CELL
    surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Maze Generator & Solver")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("monospace", 14)

    print("=" * 50)
    print("  MAZE GENERATOR & SOLVER")
    print(f"  Grid: {R} rows × {C} columns")
    print("  Generating maze with DFS mouse...")
    print("=" * 50)

    start_row = random.randrange(R)
    end_row   = random.randrange(R)

    # ── Phase 1: Generate ──
    generate_maze_animated(surface, clock, start_row, end_row)
    print("  Maze generated!")

    # Brief pause so the user can admire the maze
    pause_start = time.time()
    while time.time() - pause_start < 1.0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

    print("  Solving maze with backtracking...")

    #Phase 2: Solve
    path = solve_maze_animated(surface, clock, start_row, end_row)

    if path:
        print(f"  Solved! Path length: {len(path)} cells.")
    else:
        print("  No solution found.")

    print("  Close the window to quit.")

    # it keeps window open until user closes it
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(30)


if __name__ == "__main__":
    main()
