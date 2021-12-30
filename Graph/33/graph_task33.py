def load_matrix(filename):
    with open(filename) as f:
        matrix = []
        for line in f.readlines():
            matrix.append(list(map(int, line.split())))
            
        return matrix

def DFS(adj_matrix: list[list[int]]) -> list[list[int]]:
    def _dfs(node: int, known_nodes: set[int]):
        paths = []
        for adj_node, adj in enumerate(adj_matrix[node]):
            if adj <= 0:
                continue
            
            if adj_node in known_nodes:
                paths.append([node, adj_node])
                continue
            
            a = _dfs(adj_node, known_nodes | set([adj_node]))
            
            paths.extend([[node, *path] for path in a])

        return paths if paths else [[node]]
    
    known_nodes = set()
    paths = []
    for node in range(len(adj_matrix)):
        if node not in known_nodes:
            known_nodes.add(node)
            paths.extend(_dfs(node, set([node])))
    
    return paths

def find_cycles(paths: list[list[int]]):
    return [path for path in paths if path[0] == path[-1]]

matrix = load_matrix('graph_task33.txt')
paths = DFS(matrix)
cycles = find_cycles(paths)
print("Количество циклов:", len(cycles))
print("Циклы:")
print("\n".join(["->".join(map(str, cycle)) for cycle in cycles]))