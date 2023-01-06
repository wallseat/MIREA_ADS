from Graph.abc.graph import T_ADJ_MATRIX, T_PATH, Graph, List


# START
def task(graph: Graph) -> None:
    def get_cycles(adj_matrix: T_ADJ_MATRIX) -> List[T_PATH]:
        n = len(adj_matrix)
        cycles = []

        def _bfs(v: int) -> List[T_PATH]:
            queue = [(v, [v])]
            visited = set()

            while queue:
                i, path = queue.pop(0)
                for j in range(n):
                    if adj_matrix[i][j]:
                        if j == v:
                            cycles.append(path + [j])
                        elif j not in visited:
                            queue.append((j, path + [j]))
                            visited.add(j)

        for i in range(n):
            _bfs(i)

        return cycles

    adj_matrix = graph.to_adj_matrix()
    cycles = get_cycles(adj_matrix)

    print(f"Количество циклов: {len(cycles)}")
    print(f"Варианты обхода образующие циклы:")
    print("\n".join(["->".join(map(str, cycle)) for cycle in cycles]))


# END
