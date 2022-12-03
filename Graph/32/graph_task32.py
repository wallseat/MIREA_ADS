def read_edge_list(filename: str):
    with open(filename, "r") as f:
        dim = int(f.readline().strip())

        matrix = [[0] * dim for _ in range(dim)]

        for line in f.readlines():
            v1, v2, l = map(int, line.split())
            matrix[v1][v2] = l

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
        skip = False
        for j, l in enumerate(row):
            if l == 0 and j != i:
                skip = True
                break
        if skip:
            continue

        else:
            max_distances.append((i, max(row)))

    max_distances.sort(key=lambda tup: tup[1])

    return max_distances[0]


if __name__ == "__main__":
    from pprint import pprint

    matrix = read_edge_list("graph_task32.txt")
    distance_matrix = BFS(matrix)
    print("Матрица расстояний:")
    pprint(distance_matrix)

    center_v, radius = find_center(distance_matrix)
    print(f"Центр графа: {center_v}, радиус: {radius}")
