from Graph.abc.graph import T_ADJ_MATRIX, T_PATH, Graph, List


# START
def task(graph: Graph) -> T_PATH:
    def get_diameter_and_chains(adj_matrix: T_ADJ_MATRIX) -> List[T_PATH]:
        n = len(adj_matrix)

        def _bfs():
            path = [[None for _ in range(n)] for _ in range(n)]
            chains = [[[] for _ in range(n)] for _ in range(n)]
            for i in range(n):
                path[i][i] = 0
                chains[i][i] = [i]
                queue = [i]
                while queue:
                    v = queue.pop(0)
                    for u in range(n):
                        if adj_matrix[v][u] != 0:
                            if path[i][u] is None:
                                path[i][u] = path[i][v] + 1
                                chains[i][u] = chains[i][v] + [u]
                                queue.append(u)
            return chains

        chains = _bfs()
        max_vertices = max([max([len(j) for j in i]) for i in chains])

        diameter_chains = []
        for i, row in enumerate(chains):
            for j, chain in enumerate(row):
                if len(chain) == max_vertices and j > i:
                    diameter_chains.append(chain)

        return max_vertices - 1, diameter_chains

    adj_matrix = graph.to_adj_matrix()
    diameter, chains = get_diameter_and_chains(adj_matrix)

    print("Диаметр графа:", diameter)
    print("Цепи диаметра:", chains)


# END
