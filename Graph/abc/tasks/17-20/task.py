from Graph.abc.graph import T_ADJ_MATRIX, T_PATH, Graph, List


# START
def task(graph: Graph) -> None:
    def find_strongly_connected_components(adj_matrix: T_ADJ_MATRIX) -> List[T_PATH]:
        n = len(adj_matrix)
        used = [False] * n
        order = []
        component = []
        components = []

        def dfs1(v):
            used[v] = True
            for u in range(n):
                if adj_matrix[v][u] != 0 and not used[u]:
                    dfs1(u)
            order.append(v)

        def dfs2(v):
            used[v] = True
            component.append(v)
            for u in range(n):
                if adj_matrix[u][v] != 0 and not used[u]:
                    dfs2(u)

        for i in range(n):
            if not used[i]:
                dfs1(i)

        used = [False] * n
        for i in range(n):
            v = order[n - i - 1]
            if not used[v]:
                dfs2(v)
                components.append(component)
                component = []

        return components

    adj_matrix = graph.to_adj_matrix()
    components = find_strongly_connected_components(adj_matrix)
    print("Количество компонент сильной связности:", len(components))
    print("Компоненты сильной связности:")
    print("\n".join("->".join([str(j) for j in c]) for c in components))


# END
