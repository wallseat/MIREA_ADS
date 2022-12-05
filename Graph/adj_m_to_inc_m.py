import json


def load_adj_m(file_path: str):
    with open(file_path, "r") as f:
        matrix = []
        for line in f.readlines():
            row_data = list(map(int, line.split()))
            if len(row_data) == 1:
                continue

            matrix.append(row_data)

    return matrix


def save_as_inc_m(matrix: list[list[int]], file_path: str):
    dim = len(matrix)
    inc_matrix = []

    for i, v in enumerate(matrix):
        for j, e in enumerate(v):
            inc = [0] * dim
            if i > j:
                continue

            inc[i] = matrix[i][j] if matrix[i][j] > 0 else -1
            inc[j] = matrix[j][i] if matrix[j][i] > 0 else -1

            if sum(inc) >= 0:
                inc_matrix.append(inc)

    with open(file_path, "w") as f:
        json.dump(
            {
                "dim": len(matrix),
                "format": "inc_matrix",
                "data": [
                    [inc_matrix[i][j] for i in range(len(inc_matrix))]
                    for j in range(dim)
                ],
            },
            f,
        )


if __name__ == "__main__":
    import sys

    file_path_load = sys.argv[1]
    file_path_save = sys.argv[2]
    save_as_inc_m(load_adj_m(file_path_load), file_path_save)
