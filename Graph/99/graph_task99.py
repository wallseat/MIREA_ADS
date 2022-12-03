from typing import Tuple, List

COLORS = {1: "RED", 2: "GREEN", 3: "BLUE", 4: "YELLOW", 5: "BLACK", 6: "PURPLE"}


def read_adj_list(file_path: str):
    with open(file_path, "r") as f:
        dim = int(f.readline().strip())
        matrix = [[0] * dim for _ in range(dim)]

        for i, line in enumerate(f.readlines()):
            for adj in line.split():
                adj = int(adj)
                matrix[i][adj] = 1

    return matrix


def colorize(matrix: List[List[int]]) -> Tuple[int, List[Tuple[int, int]]]:
    v_power = [(i, sum(row)) for i, row in enumerate(matrix)]
    v_power.sort(key=lambda tup: -tup[1])
    v_color = []
    colored = set()

    color = 0
    for v1, _ in v_power:
        if v1 in colored:
            continue

        color += 1
        colored_on_step = set()

        for v2, _ in v_power:
            if v2 in colored:
                continue

            need_skip = False
            for v3 in colored_on_step:
                if matrix[v2][v3]:
                    need_skip = True
                    break

            if need_skip:
                continue

            colored_on_step.add(v2)
            v_color.append((v2, color))

        colored.update(colored_on_step)

    v_color.sort(key=lambda tup: tup[0])

    return color, v_color


if __name__ == "__main__":
    matrix = read_adj_list("graph_task99.txt")
    colors, node_color = colorize(matrix)

    print(f"Хроматическое число графа: {colors}")
    print("Пример раскраски:")
    for node, color in node_color:
        print(f"{node}: {COLORS[color]}")
