from Graph.abc.graph import T_ADJ_MATRIX, T_PATH, Graph, List


# START
def task(graph: Graph) -> None:
    def find_cycles(adj_matrix: T_ADJ_MATRIX) -> List[T_PATH]:
        n = len(adj_matrix)
        cycles = []

        for start_vertex in range(n):
            queue = [(start_vertex, [start_vertex])]
            visited = set()

            while queue:
                vertex, path = queue.pop(0)
                for neighbor in range(n):
                    if adj_matrix[vertex][neighbor] and neighbor not in visited:
                        if neighbor == start_vertex:
                            cycles.append(path + [neighbor])
                        else:
                            queue.append((neighbor, path + [neighbor]))
                            visited.add(neighbor)

        return cycles

    adj_matrix = graph.to_adj_matrix()
    cycles = find_cycles(adj_matrix)

    print(f"Количество циклов: {len(cycles)}")
    print(f"Варианты обхода образующие циклы:")
    print("\n".join(["->".join(map(str, cycle)) for cycle in cycles]))


# END
