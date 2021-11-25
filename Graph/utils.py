T_adj_list = list[tuple[int, int]]
T_adj_matrix = list[list[int]]

def matrix_to_list(matrix: T_adj_matrix) -> T_adj_list:
    return [(node, i_node) for node, inc_list in enumerate(matrix) for i_node, incident in enumerate(inc_list) if incident]       

def sort_adj_list(adj_list: T_adj_list) -> T_adj_list:
    return sorted(adj_list)

def load_matrix(i_filename: str) -> T_adj_matrix:
    with open(i_filename, 'r') as f:
        adj_matrix = [list(map(int, row.split())) for row in f]

    return adj_matrix

def load_list(i_filename: str) -> T_adj_list:
    with open(i_filename, 'r') as f:
        adj_list = [tuple(map(int, line.split())) for line in f]
    return adj_list  
    

def write_list(o_filename: str, adj_list: T_adj_list):
    with open(o_filename, 'w') as f:
        f.write("\n".join([" ".join(map(str, adj)) for adj in adj_list]))