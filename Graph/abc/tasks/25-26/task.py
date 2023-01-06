from Graph.abc.graph import T_ADJ_MATRIX, T_PATH, Graph, List

# START
T_DISTANCE_MATRIX = List[List[int]]


def task(graph: Graph) -> None:
    def get_distance_matrix(adj_matrix: T_ADJ_MATRIX) -> T_DISTANCE_MATRIX:
        n = len(adj_matrix)

        distance_matrix = [[0] * n for _ in range(n)]

        def _bfs(v: int):
            queue = [v]
            visited = set()
            while queue:
                i = queue.pop(0)
                for j in range(n):
                    if j in visited:
                        continue

                    if adj_matrix[i][j]:
                        distance = adj_matrix[i][j] + distance_matrix[v][i]
                        distance_matrix[v][j] = distance

                        queue.append(j)
                        visited.add(j)

        for i in range(n):
            _bfs(i)

        return distance_matrix

    def find_center(distance_matrix: T_DISTANCE_MATRIX) -> int:
        max_distances = []

        for i, row in enumerate(distance_matrix):
            if min(row) == 0:
                continue
            else:
                row[i] = 0
                max_distances.append((i, max(row)))

        max_distances.sort(key=lambda tup: tup[1])

        return max_distances[0]

    def find_chains(adj_matrix: T_ADJ_MATRIX, v: int, distance: int) -> List[T_PATH]:
        stack = []
        chains = []

        def _dfs(v: int, _distance: int):
            stack.append(v)
            for i, e in enumerate(adj_matrix[v]):
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

    adj_matrix = graph.to_adj_matrix()

    distance_matrix = get_distance_matrix(adj_matrix)
    center_v, radius = find_center(distance_matrix)
    print(f"Центр графа: {center_v}, радиус: {radius}")

    chains = find_chains(adj_matrix, center_v, radius)
    print("Цепи соответствующие радиусу:")
    print("\n".join("->".join(map(str, chain)) for chain in chains))


# END
