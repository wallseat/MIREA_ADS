from pprint import pprint

T_graph_paths = list[list[int]]
T_adj_list = list[tuple[int, int]]

def load_list(i_filename: str) -> T_adj_list:
    with open(i_filename, 'r') as f:
        adj_list = [tuple(map(int, line.split())) for line in f]
    return adj_list  

adj_list = load_list('graph_list.txt')

def DFS(adj_list: T_adj_list) -> T_graph_paths:
    def _dfs(node: int, known_nodes: set[int]):
        paths = []
        for adj in adj_list:
            if adj[0] != node:
                continue
            
            if adj[1] in known_nodes:
                paths.append([node, adj[1]])
                continue
            
            a = _dfs(adj[1], known_nodes | set([adj[1]]))
            
            paths.extend([[node, *path] for path in a])

        return paths if paths else [[node]]
    
    known_nodes = set()
    paths = []
    for adj in adj_list:
        if adj[0] not in known_nodes:
            known_nodes.add(adj[0])
            paths.extend(_dfs(adj[0], set([adj[0]])))
    
    return paths

def find_cycles(paths: T_graph_paths):
    return [path for path in paths if path[0] == path[-1]]

paths = DFS(adj_list)

pprint(paths)

cycles = find_cycles(paths)

pprint((cycles, len(cycles)))