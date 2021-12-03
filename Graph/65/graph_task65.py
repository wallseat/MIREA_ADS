T_adj_matrix = list[list[int]]
GraphPath = list[int]


def load_matrix(i_filename: str) -> T_adj_matrix:
    with open(i_filename, 'r') as f:
        adj_matrix = [list(map(int, row.split())) for row in f]

    return adj_matrix

def get_cycles_with_fix_len(path_len: int, matrix: T_adj_matrix) -> list[GraphPath]:
    
    def algo(node: int, len_credit: int, known_nodes: set[int]) -> list[GraphPath]:
        paths: list[list[int]] = []
        
        for other_node, edge_len in enumerate(matrix[node]):
            
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
    
    cycles = []
    for i in range(len(matrix)):
        cycles.extend(algo(i, path_len, set([i])))
        
    return cycles

if __name__ == '__main__':
    
    import sys
    
    def param_to_cycle_len(param: str) -> int:
        if not param.isdigit():
            raise Exception("Введена длина цикла не являющаяся числом!")
        
        cycle_len = int(param)
        
        if cycle_len < 3:
            raise Exception("Длина цикла не может быть меньше 3!")
        
        return cycle_len

    matrix_file = 'graph_matrix.txt'
    
    if len(sys.argv) == 2:
       cycle_len = param_to_cycle_len(sys.argv[1])
        
    elif len(sys.argv) == 3:
        matrix_file = sys.argv[1]
        cycle_len = param_to_cycle_len(sys.argv[2])
    
    else:
        raise Exception("Неверное количество аргументов!")
    

    adj_matrix = load_matrix(matrix_file)
    cycles = get_cycles_with_fix_len(cycle_len, adj_matrix)

    print(f"Циклы длины {cycle_len}: " + ", ".join(["->".join(map(str, cycle)) for cycle in cycles]))
