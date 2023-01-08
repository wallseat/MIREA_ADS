def load(self, filename: str) -> None:
    # START
    data = []
    with open(filename, "r") as file:
        dim = int(file.readline())
        for line in file.readlines():
            data.append([int(x) for x in line.split()])

    self._init_vertices(dim)
    for i, adj in enumerate(data):
        for j in adj:
            self.add_e(i, j, 1)
    # END
