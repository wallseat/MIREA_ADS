from Graph.abc.graph import T_ADJ_MATRIX, T_PATH, Graph, List, Tuple

# START
T_DISTANCE_MATRIX = List[List[T_PATH]]


def task(graph: Graph) -> None:
    def get_distances_matrix(adj_matrix: T_ADJ_MATRIX) -> T_DISTANCE_MATRIX:
        n = len(adj_matrix)

        def _bfs(start: int) -> List[T_PATH]:
            visited = [start]
            queue = [(start, [])]
            paths = [None] * n

            while queue:
                v, path = queue.pop(0)
                for i, l in enumerate(adj_matrix[v]):
                    if l and i not in visited:
                        n_path = path + [i]
                        paths[i] = n_path

                        queue.append((i, n_path))
                        visited.append(i)

            return paths

        distance_matrix: T_DISTANCE_MATRIX = []
        for i in range(n):
            distance_matrix.append(_bfs(i))

        return distance_matrix

    def get_diameter_and_chains(distance_matrix: T_DISTANCE_MATRIX) -> Tuple[int, List[T_PATH]]:
        diameter, chains = 0, []
        for row in distance_matrix:
            for path in row:
                if path is not None:
                    if len(path) > diameter:
                        diameter = len(path)
                        chains = [path]
                    elif len(path) == diameter:
                        chains.append(path)

        return diameter, chains

    adj_matrix = graph.to_adj_matrix()
    distance_matrix = get_distances_matrix(adj_matrix)
    diameter, chains = get_diameter_and_chains(distance_matrix)

    print("Диаметр графа:", diameter)
    print("Цепи диаметра:", chains)


# END
