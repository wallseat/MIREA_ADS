import copy
import random
from math import pow


def contract(vertices, edges):
    while len(vertices) > 2:
        ind = random.randrange(0, len(edges))
        u, v = edges.pop(ind)
        vertices.remove(v)
        new_edges = []
        for i in range(len(edges)):
            if edges[i][0] == v:
                edges[i][0] = u
            elif edges[i][1] == v:
                edges[i][1] = u
            if edges[i][0] != edges[i][1]:
                new_edges.append(edges[i])
        edges = new_edges

    return len(edges)


def prepare(filename: str):
    with open(filename, "r") as f:
        dim = int(f.readline().strip())
        vertices = [i for i in range(dim)]
        edges = [list(map(int, line.split())) for line in f.readlines()]

    return vertices, edges


if __name__ == "__main__":
    result = []

    vertices, edges = prepare("graph_task85.txt")

    for i in range(int(pow(len(vertices), 2))):
        v = copy.deepcopy(vertices)
        e = copy.deepcopy(edges)
        r = contract(v, e)
        result.append(r)

    print("Минимальный разрез данной сети равен:", min(result))
