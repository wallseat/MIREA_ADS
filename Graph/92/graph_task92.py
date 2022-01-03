def read_inc_matrix(filename):
    with open(filename, 'r') as f:
        dim = int(f.readline().strip())
        matrix = [[0] * dim for _ in range(dim)]

        inc_matrix = []
        for line in f.readlines():
            inc_matrix.append(list(map(int, line.split())))

        for i in range(len(inc_matrix[0])):
            first = None
            second = None

            for j in range(dim):
                if inc_matrix[j][i] != 0:
                    if inc_matrix[j][i] < 0:
                        second = j
                    else:
                        first = j

                    if first and second:
                        break

            matrix[first][second] = 1

    return matrix, dim, len(inc_matrix[0])

def bfs(matrix):
    
    bfs_queue = [0]
    visited = set()
    cycles_count = 0
    while bfs_queue:
        for i, e in enumerate(matrix[bfs_queue.pop(0)]):
            if not e:
                continue
            
            if i in visited:
                cycles_count += 1
                
            else:
                bfs_queue.append(i)
                visited.add(i)
    
    return cycles_count
                    

matrix, v, e = read_inc_matrix('graph_task92.txt')
cycles_count = bfs(matrix)

print(f"Количество вершин: {v}")
print(f"Количество граней: {e}")
print(f"Количество циклов: {cycles_count}")
print(f"Цикломатическая сложность графа: {e - v + 2 * cycles_count}")