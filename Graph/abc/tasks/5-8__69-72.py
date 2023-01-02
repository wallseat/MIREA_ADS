from Graph.abc.graph import T_ADJ_MATRIX, T_PATH, Graph, List


def task(graph: Graph) -> None:
    def bfs(adj_matrix: T_ADJ_MATRIX, path_len: int) -> List[T_PATH]:
        queue = [0]
        paths = []
        visited = set(queue)

        def _bfs(node: int, path: List[int], length: int, visited: set[int]):
            if length == path_len:
                paths.append(path)
                return

            for i, neighbor in enumerate(adj_matrix[node]):
                if i not in visited and neighbor:
                    queue.append(i)
                    _bfs(i, path + [i], length + 1, visited | set([i]))

            queue.pop(0)

        _bfs(0, [0], 0, visited)

        return paths

    adj_matrix = graph.to_adj_matrix()
    path_len = int(input("Введите длину пути: "))

    paths = bfs(adj_matrix, path_len)

    print(
        f"Все незамкнутые пути длины {path_len}:\n" + "\n".join("->".join(map(str, path)) for path in paths)
    )
