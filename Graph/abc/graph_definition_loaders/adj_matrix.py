def load(self, filename: str) -> None:
    # START
    data = []
    with open(filename, "r") as file:
        dim = int(file.readline())
        for line in file.readlines():
            data.append([int(x) for x in line.split()])

    self._init_vertices(dim)
    for i, vertex in enumerate(data):
        for j, edge_len in enumerate(vertex):
            if edge_len > 0:
                self.add_e(i, j, edge_len)
    # END
