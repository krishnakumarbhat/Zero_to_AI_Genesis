import heapq


GRID = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
]
START = (0, 0)
GOAL = (4, 4)


def h(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighbors(r, c):
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(GRID) and 0 <= nc < len(GRID[0]) and GRID[nr][nc] == 0:
            yield nr, nc


def astar(start, goal):
    pq = [(0, start)]
    g = {start: 0}
    parent = {start: None}

    while pq:
        _, cur = heapq.heappop(pq)
        if cur == goal:
            break
        for nb in neighbors(*cur):
            tentative = g[cur] + 1
            if nb not in g or tentative < g[nb]:
                g[nb] = tentative
                f = tentative + h(nb, goal)
                heapq.heappush(pq, (f, nb))
                parent[nb] = cur

    if goal not in parent:
        return []
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    return path[::-1]


def main():
    print("\nSeason 4 / Ep 01 - A* Pathfinding")
    print("Path:", astar(START, GOAL))


if __name__ == "__main__":
    main()
