from Graph.abc.graph import T_ADJ_MATRIX, T_PATH, Graph, List


# START
def task(graph: Graph) -> None:
    def dfs(adj_matrix: T_ADJ_MATRIX, s: int, e: int) -> List[T_PATH]:
        n = len(adj_matrix)
        paths = []

        def _dfs(e: int, cur_path: T_PATH) -> None:
            v = cur_path[-1]
            for i in range(n):
                if adj_matrix[v][i] and i not in cur_path:
                    if i == e:
                        paths.append(cur_path + [i])
                    else:
                        _dfs(e, cur_path + [i])

        _dfs(e, [s])

        paths.sort(key=lambda x: len(x))

        non_intersecting_paths = []
        used = set()
        for path in paths:
            if set(path).intersection(used):
                continue

            used.update(path[1:-1])
            non_intersecting_paths.append(path)

        return non_intersecting_paths

    s = int(input("Введите начальную вершину: "))
    print(s)

    e = int(input("Введите конечную вершину: "))
    print(e)

    adj_matrix = graph.to_adj_matrix()
    paths = dfs(adj_matrix, s, e)

    print(f"Не пересекающиеся пути между вершинами {s} и {e}:")
    print("\n".join(" -> ".join(str(v) for v in path) for path in paths))


# END
