DIRECTIONS = [(-1,0), (1,0), (0,-1), (0,1)]


def initialize_grid(rows, cols, dots):
    grid = [[-1] * cols for _ in range(rows)]
    for (r, c), color_id in dots.items():
        grid[r][c] = color_id
    return grid


def get_path_nodes(dots):
    starts = {}
    targets = {}
    for (r, c), color_id in dots.items():
        if color_id not in starts:
            starts[color_id] = (r, c)
        else:
            targets[color_id] = (r, c)
    return starts, targets


def is_valid_solution(grid, rows, cols, starts, targets):
    for color_id in starts:
        sr, sc = starts[color_id]
        tr, tc = targets[color_id]
        visited = set()
        queue = [(sr, sc)]
        visited.add((sr, sc))
        found = False
        while queue:
            r, c = queue.pop(0)
            if (r, c) == (tr, tc):
                found = True
                break
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and grid[nr][nc] == color_id:
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        if not found:
            return False
    return True


def count_empty(grid, rows, cols):
    return sum(1 for r in range(rows) for c in range(cols) if grid[r][c] == -1)


def solve(grid, rows, cols, path_ends, targets):
    if count_empty(grid, rows, cols) == 0:
        return is_valid_solution(grid, rows, cols,
                                  {c: path_ends[c] for c in path_ends},
                                  targets)

    color = None
    min_moves = float('inf')

    for color_id, (er, ec) in path_ends.items():
        tr, tc = targets[color_id]
        if (er, ec) == (tr, tc):
            continue
        moves = 0
        for dr, dc in DIRECTIONS:
            nr, nc = er + dr, ec + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == -1:
                    moves += 1
                elif (nr, nc) == (tr, tc):
                    moves += 1
        if moves == 0:
            return False
        if moves < min_moves:
            min_moves = moves
            color = color_id

    if color is None:
        return False

    er, ec = path_ends[color]
    tr, tc = targets[color]

    for dr, dc in DIRECTIONS:
        nr, nc = er + dr, ec + dc
        if not (0 <= nr < rows and 0 <= nc < cols):
            continue
        if grid[nr][nc] == -1:
            grid[nr][nc] = color
            path_ends[color] = (nr, nc)
            if solve(grid, rows, cols, path_ends, targets):
                return True
            grid[nr][nc] = -1
            path_ends[color] = (er, ec)
        elif (nr, nc) == (tr, tc):
            old_end = path_ends[color]
            path_ends[color] = (tr, tc)
            if solve(grid, rows, cols, path_ends, targets):
                return True
            path_ends[color] = old_end

    return False