from Graph.abc.graph import T_ADJ_MATRIX, Graph


def task(graph: Graph) -> None:
    def get_cycles_count_bfs(adj_matrix: T_ADJ_MATRIX) -> int:
        num_vertices = len(adj_matrix)
        parents = [-1] * num_vertices
        discovered = [False] * num_vertices
        processed = [False] * num_vertices
        cycles = []

        for vertex in range(num_vertices):
            if processed[vertex]:
                continue

            queue = [vertex]
            discovered[vertex] = True
            while queue:
                current_vertex = queue.pop(0)
                processed[current_vertex] = True

                for neighbor in range(num_vertices):
                    if adj_matrix[current_vertex][neighbor] and discovered[neighbor]:
                        if parents[current_vertex] != neighbor:
                            cycle = [current_vertex]
                            parent = parents[current_vertex]
                            while parent != neighbor:
                                cycle.append(parent)
                                parent = parents[parent]
                            cycle.append(neighbor)
                            cycles.append(cycle)
                    elif adj_matrix[current_vertex][neighbor] and not discovered[neighbor]:
                        discovered[neighbor] = True
                        parents[neighbor] = current_vertex
                        queue.append(neighbor)

        return len(cycles)

    cycles_count = get_cycles_count_bfs(graph.to_adj_matrix())

    v, e = len(graph.vertices), len(graph.edges)

    print(f"Количество вершин: {v}")
    print(f"Количество граней: {e}")
    print(f"Количество циклов: {cycles_count}")
    print(f"Цикломатическая сложность графа: {e - v + 2 * cycles_count}")
