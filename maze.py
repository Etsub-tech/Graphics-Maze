


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
