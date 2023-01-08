from Graph.abc.graph import T_ADJ_MATRIX, T_PATH, Graph, List


# START
def task(graph: Graph) -> None:
    def dfs(adj_matrix: T_ADJ_MATRIX, start: int, end: int) -> List[T_PATH]:
        n = len(adj_matrix)
        paths = []

        def _dfs(path: T_PATH, e: int) -> None:
            v = path[-1]
            for i in range(n):
                if adj_matrix[v][i] and i not in path:
                    n_path = path + [i]
                    if i == e:
                        paths.append(n_path)
                    else:
                        _dfs(n_path, e)

        _dfs([start], end)

        return paths

    s = int(input("Введите начальную вершину: "))
    print(s)

    e = int(input("Введите конечную вершину: "))
    print(e)

    adj_matrix = graph.to_adj_matrix()
    paths = dfs(adj_matrix, s, e)

    print(f"Все простые пути из вершины {s} в вершину {e}:")
    print("\n".join("->".join(str(v) for v in path) for path in paths))


# END
