T_adj_matrix = list[list[int]]
T_graph_paths = list[list[int]]

def load_matrix(i_filename: str) -> T_adj_matrix:
    with open(i_filename, 'r') as f:
        adj_matrix = [list(map(int, row.split())) for row in f]

    return adj_matrix

def find_paths_by_len(adj_matrix: T_adj_matrix, path_len: int) -> T_graph_paths:

    def _dfs(node: int, known_nodes: set[int], len_credit: int):
        paths = []
        for dest_node, edge_len in enumerate(adj_matrix[node]):
            
            if len_credit - edge_len < 0 or edge_len == 0:
                continue
            
            if len_credit - edge_len == 0:
                paths.append([node, dest_node])
                continue
            
            if dest_node in known_nodes:
                pass
            
            a = _dfs(dest_node, known_nodes | set([dest_node]), len_credit - edge_len)
            
            paths.extend([[node, *path] for path in a])

        return paths if paths else [[node]]
    
    paths = []
    for node in range(len(adj_matrix)):
        paths.extend(_dfs(node, set([node]), path_len))
    
    return paths


def find_cycles(paths: T_graph_paths):
    return [path for path in paths if path[0] == path[-1]]

adj_matrix = load_matrix('graph_matrix.txt')
paths = find_paths_by_len(adj_matrix, 4)
print(paths)
