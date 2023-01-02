def load_matrix(filename):
    with open(filename) as f:
        matrix = []
        for line in f.readlines():
            matrix.append(list(map(int, line.split())))

        return matrix


def DFS(matrix):
    path_stack = []

    def _dfs(v1: int):
        path_stack.append(v1)
        for v2, e in enumerate(matrix[v1]):
            if e:
                if v2 in path_stack and v2 == path_stack[0] and len(path_stack) == len(matrix):
                    path_stack.append(v2)
                    return True
                elif v2 not in path_stack:
                    if _dfs(v2):
                        return True

        path_stack.remove(v1)

    for i in range(len(matrix)):
        if _dfs(i):
            return path_stack

    return []


matrix = load_matrix("graph_task55.txt")
path = DFS(matrix)
if path:
    print("Путь проходящий через все вершины графа:")
    print("->".join(map(str, path)))
else:
    print("В данном графе не существует цикла проходящего через все вершины графа!")
