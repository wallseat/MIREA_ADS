from Graph.abc.graph import T_ADJ_MATRIX, Graph


# START
def task(graph: Graph) -> None:
    def bfs(adj_matrix: T_ADJ_MATRIX) -> int:
        n = len(adj_matrix)
        cycles_count = 0

        for start_vertex in range(n):
            queue = [(start_vertex, [start_vertex])]
            visited = set()

            while queue:
                vertex, path = queue.pop(0)
                for neighbor in range(n):
                    if adj_matrix[vertex][neighbor] and neighbor not in visited:
                        if neighbor == start_vertex:
                            cycles_count += 1
                        else:
                            queue.append((neighbor, path + [neighbor]))
                            visited.add(neighbor)

        return cycles_count

    adj_matrix = graph.to_adj_matrix()
    cycles_count = bfs(adj_matrix)

    v, e = len(graph.vertices), len(graph.edges)

    print(f"Количество вершин: {v}")
    print(f"Количество граней: {e}")
    print(f"Количество циклов: {cycles_count}")
    print(f"Цикломатическая сложность графа: {e - v + 2 * cycles_count}")


# END
