from Graph.abc.graph import T_ADJ_MATRIX, Graph, List

# START
T_COMPONENT = set[int]


def task(graph: Graph) -> None:
    def find_cuts(adj_matrix: T_ADJ_MATRIX) -> List[T_COMPONENT]:
        n = len(adj_matrix)

        def dfs(v: int, component: T_COMPONENT) -> None:
            component.add(v)
            for i in range(n):
                if adj_matrix[v][i] and i not in component:
                    dfs(i, component)

        cuts = []
        for v in range(n):
            component = set()
            dfs(v, component)
            cuts.append(component)

        return cuts

    adj_matrix = graph.to_adj_matrix()
    cuts = find_cuts(adj_matrix)
    print("Разрезы сети:\n" + "\n".join([str(cut) for cut in cuts]))


# END
