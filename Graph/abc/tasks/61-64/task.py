from Graph.abc.graph import T_ADJ_MATRIX, T_PATH, Graph, List


# START
def task(graph: Graph) -> None:
    def dfs(adj_matrix: T_ADJ_MATRIX) -> List[T_PATH]:
        n = len(adj_matrix)
        paths = []

        def _dfs(path: T_PATH) -> None:
            v = path[-1]
            for i in range(n):
                if adj_matrix[v][i] and i not in path:
                    n_path = path + [i]
                    paths.append(n_path)
                    _dfs(n_path)

        for i in range(n):
            _dfs([i])

        return paths

    adj_matrix = graph.to_adj_matrix()
    paths = dfs(adj_matrix)
    print("Все простые пути:")
    print("\n".join("->".join(str(v) for v in path) for path in paths))


# END
