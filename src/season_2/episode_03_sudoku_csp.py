Grid = list[list[int]]


def find_empty(grid: Grid):
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return r, c
    return None


def valid(grid: Grid, r: int, c: int, num: int) -> bool:
    if any(grid[r][x] == num for x in range(9)):
        return False
    if any(grid[x][c] == num for x in range(9)):
        return False
    br, bc = (r // 3) * 3, (c // 3) * 3
    for i in range(br, br + 3):
        for j in range(bc, bc + 3):
            if grid[i][j] == num:
                return False
    return True


def solve(grid: Grid) -> bool:
    spot = find_empty(grid)
    if not spot:
        return True
    r, c = spot
    for num in range(1, 10):
        if valid(grid, r, c, num):
            grid[r][c] = num
            if solve(grid):
                return True
            grid[r][c] = 0
    return False


def print_grid(grid: Grid):
    for row in grid:
        print(" ".join(str(v) for v in row))


def main():
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    print("\nSeason 4 / Ep 03 - Sudoku CSP")
    if solve(puzzle):
        print_grid(puzzle)
    else:
        print("No solution found")


if __name__ == "__main__":
    main()
