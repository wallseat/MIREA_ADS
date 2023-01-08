def load(self, filename: str) -> None:
    # START
    data = []
    with open(filename, "r") as file:
        dim = int(file.readline())
        for line in file.readlines():
            data.append([int(x) for x in line.split()])

    self._init_vertices(dim)

    transposed_data = list(zip(*data))  # транспонирование

    for edge in transposed_data:
        v1 = None
        v2 = None
        v1_v2_len = 0
        v2_v1_len = 0
        for j in range(dim):
            if edge[j] != 0 and v1 is None:
                v1 = j
                v1_v2_len = edge[j]
            elif edge[j] != 0 and v2 is None:
                v2 = j
                v2_v1_len = edge[j]
                break

        if v1_v2_len > 0:
            self.add_e(v1, v2, v1_v2_len)

        if v2_v1_len > 0:
            self.add_e(v2, v1, v2_v1_len)
    # END
