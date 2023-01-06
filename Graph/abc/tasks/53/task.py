from Graph.abc.graph import T_ADJ_MATRIX, T_PATH, Graph, List, Optional

# START


def task(graph: Graph) -> None:
    def find_path_through_all_edges(adj_matrix: T_ADJ_MATRIX) -> T_PATH:
        n = len(adj_matrix)

        def _dfs(v: int, path: List[int]) -> Optional[T_PATH]:
            for j in range(n):
                if j not in path and adj_matrix[v][j]:
                    n_path = path + [j]
                    if len(n_path) == n:
                        if not adj_matrix[path[0]][j] and not adj_matrix[j][path[0]]:
                            return n_path
                    else:
                        if out_path := _dfs(j, n_path):
                            return out_path

        for i in range(n):
            if out_path := _dfs(i, [i]):
                return out_path

    adj_matrix = graph.to_adj_matrix()
    path = find_path_through_all_edges(adj_matrix)

    if path:
        print("Путь проходящий через все вершины орграфа:\n" + "->".join(map(str, path)))
    else:
        print("Пути проходящие через все вершины орграфа не существует")


# END
