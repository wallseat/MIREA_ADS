from typing import List


def read_inc_matrix(filename):
    with open(filename, "r") as f:
        dim = int(f.readline().strip())
        matrix = [[0] * dim for _ in range(dim)]

        inc_matrix = []
        for line in f.readlines():
            inc_matrix.append(list(map(int, line.split())))

        for i in range(len(inc_matrix[0])):
            first = None
            first_e = 0
            second = None
            second_e = 0

            for j in range(dim):
                if inc_matrix[j][i] != 0:
                    if first is None:
                        first = j
                        if inc_matrix[j][i] > 0:
                            first_e = inc_matrix[j][i]
                    else:
                        second = j
                        if inc_matrix[j][i] > 0:
                            second_e = inc_matrix[j][i]

                    if first and second:
                        break

            if first_e:
                matrix[first][second] = first_e
            if second_e:
                matrix[second][first] = second_e

    return matrix


def BFS(matrix):
    distance_matrix = [[0] * len(matrix) for i in range(len(matrix))]

    def _bfs(v: int):
        queue = [v]
        visited = set()
        while queue:
            cur_node = queue.pop(0)
            for i, e in enumerate(matrix[cur_node]):
                if i in visited:
                    continue

                if e > 0:
                    distance = e + distance_matrix[v][cur_node]
                    distance_matrix[v][i] = distance

                    queue.append(i)
                    visited.add(i)

    for i in range(len(matrix)):
        _bfs(i)

    return distance_matrix


def find_center(matrix):
    max_distances = []

    for i, row in enumerate(matrix):
        if min(row) == 0:
            continue
        else:
            max_distances.append((i, max(row)))

    max_distances.sort(key=lambda tup: tup[1])

    return max_distances[0]


def find_chains(matrix: List[List[int]], v: int, distance: int):
    stack = []
    chains = []

    def _dfs(v: int, _distance: int):
        stack.append(v)
        for i, e in enumerate(matrix[v]):
            if i in stack:
                continue
            if e:
                if _distance - e == 0:
                    chains.append([*stack.copy(), i])
                elif _distance - e >= 0:
                    _dfs(i, _distance - e)

        stack.remove(v)

    _dfs(v, distance)

    return chains


if __name__ == "__main__":
    from pprint import pprint

    matrix = read_inc_matrix("graph_task30.txt")
    distance_matrix = BFS(matrix)
    print("Матрица расстояний:")
    pprint(distance_matrix)

    center_v, radius = find_center(distance_matrix)
    print(f"Центр графа: {center_v}, радиус: {radius}")

    chains = find_chains(matrix, center_v, radius)
    print("Цепи соответствующие радиусу:")
    print("\n".join("->".join(map(str, chain)) for chain in chains))
