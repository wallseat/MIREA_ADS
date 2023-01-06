from Graph.abc.graph import T_ADJ_MATRIX, T_PATH, Graph, List, Optional, Tuple

# START
T_EDGES_SET = set[Tuple[int, int]]


def task(graph: Graph) -> None:
    def find_path_through_all_edges(adj_matrix: T_ADJ_MATRIX) -> T_PATH:
        n = len(adj_matrix)

        edges: T_EDGES_SET = {(i, j) for i in range(n) for j in range(n) if adj_matrix[i][j] != 0}

        def _dfs(v: int, remaining_edges: T_EDGES_SET, path: List[int]) -> Optional[T_PATH]:
            for j in range(n):
                if adj_matrix[v][j] and (v, j) in remaining_edges:
                    n_remaining_edges = remaining_edges - {(v, j)}
                    n_path = path + [j]
                    if not n_remaining_edges:
                        if path[0] != j and not adj_matrix[path[0]][j] and not adj_matrix[j][path[0]]:
                            return n_path
                    else:
                        if out_path := _dfs(j, n_remaining_edges, n_path):
                            return out_path

        for i in range(n):
            if out_path := _dfs(i, edges, [i]):
                return out_path

    adj_matrix = graph.to_adj_matrix()
    path = find_path_through_all_edges(adj_matrix)

    if path:
        print("Путь проходящий через все ребра орграфа:\n" + "->".join(map(str, path)))
    else:
        print("Пути проходящие через все ребра орграфа не существует")


# END
