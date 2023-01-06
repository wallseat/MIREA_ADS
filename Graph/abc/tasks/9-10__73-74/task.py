# START
import copy

from Graph.abc.graph import T_ADJ_MATRIX, Graph


def task(graph: Graph) -> None:
    def transitive_reduction(adj_matrix: T_ADJ_MATRIX) -> T_ADJ_MATRIX:
        n = len(adj_matrix)
        out_matrix = copy.deepcopy(adj_matrix)

        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if (i, j) == (j, k) or (i, j) == (i, k):
                        continue
                    if adj_matrix[i][j] and adj_matrix[j][k]:
                        out_matrix[i][k] = 0

        return out_matrix

    adj_matrix = graph.to_adj_matrix()
    reduced_adj_matrix = transitive_reduction(adj_matrix)

    print("Исходная матрица смежности графа G:")
    print("\n".join(" ".join(map(str, row)) for row in adj_matrix))
    print("Для заданного графа G матрица смежности графа G':")
    print("\n".join(" ".join(map(str, row)) for row in reduced_adj_matrix))


# END
