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


def save_as_adj_list(matrix: list[list[int]], file_path: str):
    with open(file_path, "w") as f:
        json.dump(
            {
                "dim": len(matrix),
                "format": "adj_list",
                "data": ([[i for i, el in enumerate(row) if el] for row in matrix]),
            },
            f,
        )


if __name__ == "__main__":
    import sys

    file_path_load = sys.argv[1]
    file_path_save = sys.argv[2]
    save_as_adj_list(load_adj_m(file_path_load), file_path_save)
