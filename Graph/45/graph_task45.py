def load_matrix(filename):
    with open(filename) as f:
        matrix = []
        for line in f.readlines():
            matrix.append(list(map(int, line.split())))

        return matrix


def DFS(matrix):
    path_stack = []
    paths = []

    def _dfs(v1: int):
        path_stack.append(v1)
        for v2, e in enumerate(matrix[v1]):
            if e > 0 and not v2 in path_stack:
                _dfs(v2)

        if len(path_stack) > 1:
            paths.append(path_stack.copy())

        path_stack.remove(v1)

    for v in range(len(matrix)):
        _dfs(v)

    return sorted(paths)


matrix = load_matrix("graph_task45.txt")
paths = DFS(matrix)
print("Количество путей:", len(paths))
print("Пути:")
print("\n".join(["->".join(map(str, path)) for path in paths]))
