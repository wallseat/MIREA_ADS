from Graph.abc.graph import T_ADJ_MATRIX, T_PATH, Graph, List


# START
def task(graph: Graph) -> None:
    def get_all_paths(adj_matrix: T_ADJ_MATRIX) -> List[T_PATH]:
        n = len(adj_matrix)

        paths = []

        def _dfs(v: int, path: T_PATH) -> None:
            for i in range(n):
                if adj_matrix[v][i] and i not in path:
                    n_path = path + [i]
                    paths.append(n_path)
                    _dfs(i, n_path)

        for i in range(n):
            _dfs(i, [i])

        return paths

    adj_matrix = graph.to_adj_matrix()
    paths = get_all_paths(adj_matrix)

    print("Количество путей:", len(paths))
    print("Пути:")
    print("\n".join(["->".join(map(str, path)) for path in paths]))


# END
