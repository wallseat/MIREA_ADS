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


def save_adj_m(matrix: list[list[int]], file_path: str):
    with open(file_path, "w") as f:
        json.dump({"dim": len(matrix), "format": "adj_matrix", "data": matrix}, f)


if __name__ == "__main__":
    import sys

    file_path_load = sys.argv[1]
    file_path_save = sys.argv[2]
    save_adj_m(load_adj_m(file_path_load), file_path_save)
