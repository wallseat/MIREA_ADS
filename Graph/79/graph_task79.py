def find_graph_k(matrix: list[list[int]]):
    graph = []
    dim = len(matrix)

    def bfs(s, t, parent):
        visited = [False] * dim

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

    def ford_fulkerson(source, sink):
        parent = [-1] * dim

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
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i == j:
                continue
            graph = [row[:] for row in matrix]
            local_k = ford_fulkerson(i, j)
            if k is None or local_k < k:
                k = local_k

    return k


with open("graph_task79.txt", "r") as f:
    matrix = list(map(list, [map(int, line.split()) for line in f.readlines()]))

print(f"K-связность графа равна: {find_graph_k(matrix)}")
