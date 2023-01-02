from typing import Set

from Graph.abc.graph import T_PATH, Graph, List


def task(graph: Graph) -> None:
    def algo(node: int, len_credit: int, known_nodes: Set[int]) -> List[T_PATH]:
        paths: List[List[int]] = []

        for other_node, edge_len in enumerate(adj_matrix[node]):

            if not edge_len:
                continue

            if not other_node in known_nodes and len_credit - edge_len > 0:
                _known_nodes = known_nodes.copy()
                _known_nodes.add(other_node)
                _paths = algo(other_node, len_credit - edge_len, _known_nodes)
                paths.extend([node, *path] for path in _paths if _paths)

            elif other_node in known_nodes and len_credit - edge_len == 0:
                paths.append([node, other_node])

        return paths

    adj_matrix = graph.to_adj_matrix()
    path_len = int(input("Введите длину пути: "))

    cycles = []
    for i in range(len(adj_matrix)):
        cycles.extend(algo(i, path_len, set([i])))

    print(f"Циклы длины {path_len}:")
    print("\n".join(["->".join(map(str, cycle)) for cycle in cycles]))
