import copy
from pprint import pprint


def read_inc_matrix(filename):
    with open(filename, "r") as f:
        dim = int(f.readline().strip())
        matrix = [[0] * dim for _ in range(dim)]

        inc_matrix = []
        for line in f.readlines():
            inc_matrix.append(list(map(int, line.split())))

        for i in range(len(inc_matrix[0])):
            first = None
            first_e = 0
            second = None
            second_e = 0

            for j in range(dim):
                if inc_matrix[j][i] != 0:
                    if first is None:
                        first = j
                        if inc_matrix[j][i] > 0:
                            first_e = inc_matrix[j][i]
                    else:
                        second = j
                        if inc_matrix[j][i] > 0:
                            second_e = inc_matrix[j][i]

                    if first and second:
                        break

            if first_e:
                matrix[first][second] = first_e
            if second_e:
                matrix[second][first] = second_e

    return matrix


def transitive_reduction(matrix):
    out_matrix = copy.deepcopy(matrix)

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            for k in range(len(matrix)):
                if (i, j) == (j, k) or (i, j) == (i, k):
                    continue
                if matrix[i][j] and matrix[j][k]:
                    out_matrix[i][k] = 0

    return out_matrix


matrix = read_inc_matrix("graph_task10.txt")
print("Исходная матрица смежности графа G:")
print("\n".join(" ".join(map(str, row)) for row in matrix))
print("Для заданного графа G матрица смежности графа G':")
print("\n".join(" ".join(map(str, row)) for row in transitive_reduction(matrix)))
