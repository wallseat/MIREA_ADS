from Graph.abc.graph import T_ADJ_MATRIX, Graph


def task(graph: Graph) -> None:
    def get_cycles_count_dfs(adj_matrix: T_ADJ_MATRIX) -> int:
        n = len(adj_matrix)
        used = [False] * n
        cycles_count = 0

        def dfs(v: int) -> None:
            nonlocal cycles_count
            used[v] = True
            for u in range(n):
                if adj_matrix[v][u] != 0:
                    if not used[u]:
                        dfs(u)
                    else:
                        cycles_count += 1

        for i in range(n):
            if not used[i]:
                dfs(i)

        return cycles_count

    cycles_count = get_cycles_count_dfs(graph.to_adj_matrix())

    v, e = len(graph.vertices), len(graph.edges)

    print(f"Количество вершин: {v}")
    print(f"Количество граней: {e}")
    print(f"Количество циклов: {cycles_count}")
    print(f"Цикломатическая сложность графа: {e - v + 2 * cycles_count}")
