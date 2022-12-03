def read_inc_matrix(filename):
    with open(filename, "r") as f:
        dim = int(f.readline().strip())
        matrix = [[0] * dim for _ in range(dim)]

        inc_matrix = []
        for line in f.readlines():
            inc_matrix.append(list(map(int, line.split())))

        for i in range(len(inc_matrix[0])):
            first = None
            second = None

            for j in range(dim):
                if inc_matrix[j][i] != 0:
                    if inc_matrix[j][i] < 0:
                        second = j
                    else:
                        first = j

                    if first and second:
                        break

            matrix[first][second] = 1

    return matrix


def graph_root(matrix):
    vertices: set

    def _dfs(v1: int):
        vertices.discard(v1)
        for v2, edge in enumerate(matrix[v1]):
            if edge == 1:
                _dfs(v2)

        return vertices

    for i in range(len(matrix)):
        vertices = set(j for j in range(len(matrix)))
        if len(_dfs(i)) == 0:
            return i

    return -1


matrix = read_inc_matrix("graph_task50.txt")
graph_root = graph_root(matrix)
if graph_root >= 0:
    print(f"Корень графа существует и является {graph_root}")
else:
    print("Корня данного графа не существует!")
