from Graph.abc.graph import T_ADJ_MATRIX, T_PATH, Graph, List, Tuple


def task(graph: Graph) -> None:
    def find_path_through_all_edges(adj_matrix: T_ADJ_MATRIX) -> T_PATH:
        n = len(adj_matrix)

        remaining_edges: set[Tuple[int, int]] = {
            (i, j) for i in range(n) for j in range(n) if adj_matrix[i][j] != 0
        }
        edge_stack: List[Tuple[int, int]] = []

        for i in range(n):
            vertices_stack: List[int] = [i]

            while vertices_stack:
                v = vertices_stack[-1]
                ret = True

                for j in range(n):
                    if not adj_matrix[v][j]:
                        if (v, j) in remaining_edges:
                            adj_matrix[v][j] = 1
                        continue

                    if (v, j) in remaining_edges:
                        remaining_edges.remove((v, j))
                        edge_stack.append((v, j))
                        vertices_stack.append(j)
                        adj_matrix[v][j] = 0
                        ret = False
                        break

                if not remaining_edges:
                    return edge_stack

                if ret:
                    vertices_stack.pop()
                    if edge_stack:
                        remaining_edges.add(edge_stack.pop())

    adj_matrix = graph.to_adj_matrix()
    path = find_path_through_all_edges(adj_matrix)

    print("Путь проходящий через все ребра орграфа:\n" + "->".join(map(str, path)))
