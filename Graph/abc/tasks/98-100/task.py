from Graph.abc.graph import Graph, List, Tuple

# START


def task(graph: Graph) -> None:
    COLORS = {1: "RED", 2: "GREEN", 3: "BLUE", 4: "YELLOW", 5: "BLACK", 6: "PURPLE"}

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

    adj_matrix = graph.to_adj_matrix()
    colors, node_color = colorize(adj_matrix)

    print(f"Хроматическое число графа: {colors}")
    print("Пример раскраски:")
    for node, color in node_color:
        print(f"{node}: {COLORS[color]}")


# END
