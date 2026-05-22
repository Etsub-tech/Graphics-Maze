


def unvisited_neighbours(r, c):
    """Return list of (nr, nc, direction) for unvisited neighbours."""
    result = []

    if r > 0 and not gen_visited[r - 1][c]:
        result.append((r - 1, c, 'N'))

    if r < R - 1 and not gen_visited[r + 1][c]:
        result.append((r + 1, c, 'S'))

    if c > 0 and not gen_visited[r][c - 1]:
        result.append((r, c - 1, 'W'))

    if c < C - 1 and not gen_visited[r][c + 1]:
        result.append((r, c + 1, 'E'))

    return result

def remove_wall(r, c, direction):

    if direction == 'N':
        northWall[r][c] = 0

    elif direction == 'S':
        northWall[r + 1][c] = 0

    elif direction == 'W':
        eastWall[r][c] = 0

    elif direction == 'E':
        eastWall[r][c + 1] = 0

def generate_maze_animated(surface, clock):

    reset_walls()

    # optional openings
    northWall[0][0] = 0
    northWall[R][C - 1] = 0

    # random starting point
    sr, sc = random.randrange(R), random.randrange(C)

    gen_visited[sr][sc] = True

    stack = [(sr, sc)]

    while stack:

        # allow window closing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        r, c = stack[-1]

        neighbours = unvisited_neighbours(r, c)

        if neighbours:

            # choose random neighbour
            nr, nc, direction = random.choice(neighbours)

            # remove wall between cells
            remove_wall(r, c, direction)

            # move forward
            gen_visited[nr][nc] = True

            stack.append((nr, nc))

        else:
            # backtrack
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


def solve_maze_animated(surface, clock):
    # cell_state: 0 means unvisited, 1 means on stack (active), 2 means dead end
    cell_state = [[0] * C for _ in range(R)]
    parent     = [[None] * C for _ in range(R)]   

    # Start at top left, end at bottom right
    start_row = random.randrange(R)
    end_row = random.randrange(R)
   
    start = (start_row, 0)
    end = (end_row, C-1)

    stack = [start]
    cell_state[0][0] = 1

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

    # ── Phase 1: Generate ──
    generate_maze_animated(surface, clock)
    print("  Maze generated!")

    # Brief pause so the user can admire the maze
    pause_start = time.time()
    while time.time() - pause_start < 1.0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

    print("  Solving maze with backtracking...")

    #Phase 2: Solve
    path = solve_maze_animated(surface, clock)

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


if name == "__main__":
    main()
