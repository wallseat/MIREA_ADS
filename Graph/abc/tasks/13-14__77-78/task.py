from Graph.abc.graph import T_ADJ_MATRIX, Graph, List, Tuple

# START
T_BRIDGE = Tuple[int, int]


def task(graph: Graph) -> None:
    def find_bridges(adj_matrix: T_ADJ_MATRIX) -> List[T_BRIDGE]:
        n = len(adj_matrix)
        bridges = []
        visited = [False] * n
        disc = [float("inf")] * n
        low = [float("inf")] * n
        parent = [-1] * n

        def dfs(u: int, time: int) -> None:
            visited[u] = True
            disc[u] = low[u] = time + 1

            for v in range(n):
                if adj_matrix[u][v] and not visited[v]:
                    parent[v] = u
                    dfs(v, time + 1)
                    low[u] = min(low[u], low[v])
                    if low[v] > disc[u]:
                        bridges.append((u, v))

                elif adj_matrix[u][v] and v != parent[u]:
                    low[u] = min(low[u], disc[v])

        for i in range(n):
            if not visited[i]:
                dfs(i, 0)

        return bridges

    adj_matrix = graph.to_adj_matrix()
    bridges = find_bridges(adj_matrix)

    print("Все мосты графа:")
    print("\n".join([str(tup) for tup in bridges]))


# END
