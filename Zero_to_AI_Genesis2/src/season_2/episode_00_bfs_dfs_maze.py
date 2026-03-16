from collections import deque


GRID = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
]
START = (0, 0)
GOAL = (4, 4)


def neighbors(r, c):
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(GRID) and 0 <= nc < len(GRID[0]) and GRID[nr][nc] == 0:
            yield nr, nc


def bfs(start, goal):
    q = deque([start])
    parent = {start: None}
    while q:
        node = q.popleft()
        if node == goal:
            break
        for nb in neighbors(*node):
            if nb not in parent:
                parent[nb] = node
                q.append(nb)
    return reconstruct(parent, goal)


def dfs(start, goal):
    stack = [start]
    parent = {start: None}
    while stack:
        node = stack.pop()
        if node == goal:
            break
        for nb in neighbors(*node):
            if nb not in parent:
                parent[nb] = node
                stack.append(nb)
    return reconstruct(parent, goal)


def reconstruct(parent, goal):
    if goal not in parent:
        return []
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    return path[::-1]


def main():
    print("\nSeason 4 / Ep 00 - BFS & DFS Maze")
    print("BFS path:", bfs(START, GOAL))
    print("DFS path:", dfs(START, GOAL))


if __name__ == "__main__":
    main()
