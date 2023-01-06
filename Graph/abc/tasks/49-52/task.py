from Graph.abc.graph import T_ADJ_MATRIX, T_PATH, Graph, List, Optional

# START


def task(graph: Graph) -> None:
    def find_root(adj_matrix: T_ADJ_MATRIX) -> int:
        n = len(adj_matrix)
        paths: List[Optional[T_PATH]]

        def _dfs(v: int, path: List[int]) -> None:
            for i in range(n):
                if i not in path and adj_matrix[v][i]:
                    n_path = path + [i]

                    if paths[i] is None:
                        paths[i] = n_path

                    _dfs(i, n_path)

        for i in range(n):
            paths = [None for _ in range(n)]
            paths[i] = [i]
            _dfs(i, [i])

            if all(paths):
                return i, paths

    adj_matrix = graph.to_adj_matrix()
    root, paths = find_root(adj_matrix)

    print(f"Корень графа: {root}")
    print("Пути до всех вершин от корня:")
    print("\n".join("->".join(str(v) for v in path) for i, path in enumerate(paths) if i != root))


# END
