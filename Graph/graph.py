T_edge_list = list[tuple[int, int]]
T_adj_matrix = list[list[int]]
T_inc_matrix = list[list[int]]

class Graph:
    labels: dict[int, str]
    matrix: T_adj_matrix
    edge_count: int
    
    def __init__(self):
        labels = {}
        matrix = None
        edge_count = 0
    
    def to_edge_list(self) -> T_edge_list:
        edge_list = []
        for node, row in enumerate(self.matrix):
            for i_node, edge_len in enumerate(row):
                edge_list.append((node, i_node, edge_len))
                
        return edge_list
    
    def to_incidence_matrix(self) -> T_inc_matrix:
        inc_matrix = [[0 for _ in range(len(self.edge_count))] for _ in range(len(self.edge_count))]
        
        cur_edge = 0 #TODO доработать класс и функцию перевода в матрицу инцендентности
        
        for node, row in enumerate(self.matrix):
            for i_node, edge_len in enumerate(row):
                if edge_len:
                    pass
             
    def load_adj_matrix(self, i_filename: str):
        with open(i_filename, 'r') as f:
            adj_matrix = [list(map(int, row.split())) for row in f]

        self.matrix = adj_matrix
        
        self._edge_count()

    def load_edge_list(self, i_filename: str):
        with open(i_filename, 'r') as f:
            edge_list = [tuple(map(int, line.split())) for line in f]
        
        dim = max(edge_list, key=lambda x, y, _: x if x > y else y) + 1
        self.matrix = [[0 for _ in range(dim)] for _ in range(dim)]
        
        for edge in edge_list:
            self.matrix[edge[0]][edge[1]] = edge[2]
        
        self._edge_count()
    
    def load_incidence_matrix(self, i_filename: str):
        with open(i_filename, 'r') as f:
            inc_matrix = [list(map(int, row.split())) for row in f]

        dim = len(inc_matrix)
        self.matrix = [[0 for _ in range(dim)] for _ in range(dim)]

        for i in range(len(inc_matrix)):
            n1, n2, n1_n2_edge_len, n2_n1_edge_len = None, None, 0, 0
            for j in range(len(inc_matrix)):
                if inc_matrix[j][i]:
                    if not n1:
                        n1 = j
                        n1_n2_edge_len = inc_matrix[j][i]
                    else:
                        n2 = j
                        n2_n1_edge_len =  inc_matrix[j][i]
                        break
            
            if n1_n2_edge_len > 0:
                self.matrix[n1][n2] = n1_n2_edge_len
            if n2_n1_edge_len > 0:
                self.matrix[n2][n1] = n2_n1_edge_len
    
        self._edge_count()
        
    def _edge_count(self):
        count = 0
        for row in self.matrix:
            for col in row:
                if col:
                    count += 1
                    
        self._edge_count = count
    
    @property
    def edge_count(self):
        return self._edge_count