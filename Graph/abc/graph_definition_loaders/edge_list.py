def load(self, filename: str) -> None:
    # START
    data = []
    with open(filename, "r") as file:
        dim = int(file.readline())
        for line in file.readlines():
            data.append([int(x) for x in line.split()])

    self._init_vertices(dim)

    for edge in data:
        if len(edge) == 3:
            v1, v2, edge_len = edge
        else:
            v1, v2, edge_len = *edge, 1

        self.add_e(v1, v2, edge_len)
    # END
