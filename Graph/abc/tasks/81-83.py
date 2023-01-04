from Graph.abc.graph import T_ADJ_MATRIX, Graph, List


def task(graph: Graph) -> None:
    def find_cuts(adj_matrix: T_ADJ_MATRIX) -> List[List[int]]:
        def dfs(node, visited):
            visited.add(node)
            for neighbor, adj in enumerate(adj_matrix[node]):
                if adj and neighbor not in visited:
                    dfs(neighbor, visited)

        cuts = []
        visited = set()
        for node in range(len(adj_matrix)):
            if node not in visited:
                component = set()
                dfs(node, component)
                cuts.append(list(component))
        return cuts

    cuts = find_cuts(graph.to_adj_matrix())
    print("Разрезы сети:\n" + "\n".join([str(cut) for cut in cuts]))
