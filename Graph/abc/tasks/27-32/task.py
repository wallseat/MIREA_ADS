from Graph.abc.graph import T_ADJ_MATRIX, T_PATH, Graph, List


# START
def task(graph: Graph):
    def get_distance_matrix(adj_matrix: T_ADJ_MATRIX) -> T_ADJ_MATRIX:
        distance_matrix = [[0] * len(adj_matrix) for _ in range(len(adj_matrix))]

        def _bfs(v: int):
            queue = [v]
            visited = set()
            while queue:
                cur_node = queue.pop(0)
                for i, e in enumerate(adj_matrix[cur_node]):
                    if i in visited:
                        continue

                    if e > 0:
                        distance = e + distance_matrix[v][cur_node]
                        distance_matrix[v][i] = distance

                        queue.append(i)
                        visited.add(i)

        for i in range(len(adj_matrix)):
            _bfs(i)

        return distance_matrix

    def find_center(adj_matrix: T_ADJ_MATRIX) -> int:
        max_distances = []

        for i, row in enumerate(adj_matrix):
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
