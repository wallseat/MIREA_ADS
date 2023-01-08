from Graph.abc.graph import T_ADJ_MATRIX, T_PATH, Graph


# START
def task(graph: Graph) -> None:
    def get_graph_k(adj_matrix: T_ADJ_MATRIX) -> int:
        graph = []
        n = len(adj_matrix)

        def bfs(s: int, t: int, parent: T_PATH) -> bool:
            visited = [False] * n

            queue = []
            queue.append(s)
            visited[s] = True

            while queue:
                u = queue.pop(0)

                for ind, val in enumerate(graph[u]):
                    if visited[ind] == False and val > 0:

                        queue.append(ind)
                        visited[ind] = True

                        parent[ind] = u
                        if ind == t:
                            return True
            return False

        def ford_fulkerson(source: int, sink: int) -> int:
            parent = [-1] * n

            max_flow = 0
            while bfs(source, sink, parent):
                path_flow = float("Inf")
                s = sink
                while s != source:
                    path_flow = min(path_flow, graph[parent[s]][s])
                    s = parent[s]

                max_flow += path_flow

                v = sink
                while v != source:
                    u = parent[v]
                    graph[u][v] -= path_flow
                    graph[v][u] += path_flow
                    v = parent[v]

            return max_flow

        k = None
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                graph = [row[:] for row in adj_matrix]
                local_k = ford_fulkerson(i, j)
                if k is None or local_k < k:
                    k = local_k

        return k

    adj_matrix = graph.to_adj_matrix()
    graph_k = get_graph_k(adj_matrix)

    print(f"K-связность графа равна: {graph_k}")


# END
