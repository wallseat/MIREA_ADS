from Graph.abc.graph import T_ADJ_MATRIX, T_PATH, Graph, List


# START
def task(graph: Graph) -> None:
    def get_cycles(adj_matrix: T_ADJ_MATRIX) -> List[T_PATH]:
        n = len(adj_matrix)
        cycles = []

        def _dfs(path_stack: T_PATH) -> List[T_PATH]:
            v = path_stack[-1]

            for i in range(n):
                if adj_matrix[v][i]:
                    if i == path_stack[0]:
                        cycles.append([*path_stack, i])
                    elif i not in path_stack:
                        _dfs([*path_stack, i])

        for i in range(n):
            _dfs([i])

        return cycles

    adj_matrix = graph.to_adj_matrix()
    cycles = get_cycles(adj_matrix)

    print(f"Количество циклов: {len(cycles)}")
    print(f"Варианты обхода образующие циклы:")
    print("\n".join(["->".join(map(str, cycle)) for cycle in cycles]))


# END
