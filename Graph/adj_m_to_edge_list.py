def load_adj_m(file_path: str):
    with open(file_path, "r") as f:
        matrix = []
        for line in f.readlines():
            row_data = list(map(int, line.split()))
            if len(row_data) == 1:
                continue

            matrix.append(row_data)

    return matrix


def save_as_edge_list(matrix: list[list[int]], file_path: str):
    edge_list = []
    for i, row in enumerate(matrix):
        for j, l in enumerate(row):
            if l:
                edge_list.append((i, j, l))

    with open(file_path, "w") as f:
        f.write(str(len(matrix)) + "\n")
        for edge in edge_list:
            f.write(" ".join(map(str, edge)) + "\n")


if __name__ == "__main__":
    import sys

    file_path_load = sys.argv[1]
    file_path_save = sys.argv[2]
    save_as_edge_list(load_adj_m(file_path_load), file_path_save)
