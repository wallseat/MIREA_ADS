from typing import Dict, List, Optional, Tuple  # noqa: F401w

T_ADJ_MATRIX = List[List[int]]
T_PATH = List[int]


class Vertex:
    _index: int

    def __init__(self, index: int) -> None:
        self._index = index

    @property
    def index(self) -> int:
        return self._index

    def __repr__(self):
        return f"Vertex[i: {self._index}]"


class Edge:
    _vertices: Tuple[int, int]
    len: int

    def __init__(self, v1: int = None, v2: int = None, len: int = 1):
        self._vertices = (v1, v2)
        self.len = len

    @property
    def vertices(self) -> Tuple[int, int]:
        return self._vertices

    def __repr__(self):
        return f"Edge[{self._vertices[0]} -> {self._vertices[1]}, {self.len}]"


class Graph:
    _vertices: List[Vertex]
    _edges: List[Edge]

    def __init__(self) -> None:
        self._vertices = []
        self._edges = []

    def _init_vertices(self, dim: int):
        self._vertices = []
        for i in range(dim):
            self._vertices.append(Vertex(i))

    def load(self, filename: str) -> None:
        pass  # LOADER

    def first(self, v: int) -> None | int:
        for edge in self._edges:
            if edge.vertices[0] == v:
                return edge.vertices[1]

        return None

    def next(self, v: int, i: int) -> None | int:
        state = 0
        next_index = None

        for edge in self._edges:
            if edge.vertices[0] != v:
                if state == 0:
                    continue
                if state == 1:
                    break
            else:
                state = 1
                if edge.vertices[1] > i:
                    next_index = edge.vertices[1]
                    break

        return next_index

    def vertex(self, v: int, i: int) -> None | int:
        state = 0
        vertices_set: List[int] = []

        for edge in self._edges:
            if edge.vertices[0] != v:
                if state == 0:
                    continue
                if state == 1:
                    break
            else:
                state = 1
                vertices_set.append(edge.vertices[1])

        if i < len(vertices_set):
            return vertices_set[i]
        else:
            return None

    def add_v(self, index: int, label: str = "") -> None:
        for vertex in self._vertices:
            if vertex.index == index:
                raise Exception(f"Вершина с таким индексом уже существует! ({index})")

        self._vertices.append(Vertex(index, label))

    def add_e(self, v1: int, v2: int, edge_len: int = 1) -> None:
        found_v1 = False
        found_v2 = False
        for vertex in self._vertices:
            if vertex.index == v1:
                found_v1 = True
            elif vertex.index == v2:
                found_v2 = True

        if not (found_v1 and found_v2) or v1 == v2:
            raise Exception(f"Невозможная пара индексов вершин! ({v1}, {v2})")

        else:
            self._edges.append(Edge(v1, v2, edge_len))

    def del_v(self, index: int) -> None:
        for vertex in self._vertices:
            if vertex.index == index:
                break
        else:
            raise Exception(f"Вершина с таким индексом не существует! ({index})")

        edges_to_remove = []
        for edge in self._edges:
            if edge.vertices[0] == index or edge.vertices[1] == index:
                edges_to_remove.append(edge)

        for edge in edges_to_remove:
            self._edges.remove(edge)

    def del_e(self, v1: int, v2: int) -> None:
        for edge in self._edges:
            if edge.vertices[0] == v1 and edge.vertices[1] == v2:
                break
        else:
            raise Exception(f"Ребра с таким набором вершин не существует! ({v1}, {v2})")

    def to_adj_matrix(self) -> T_ADJ_MATRIX:
        adj_matrix = [[0 for _ in range(len(self._vertices))] for _ in range(len(self._vertices))]
        for edge in self._edges:
            adj_matrix[edge._vertices[0]][edge._vertices[1]] = edge.len

        return adj_matrix

    def as_dict(self) -> Dict:
        return {"Vertices": self._vertices, "Edges": self._edges}

    @property
    def vertices(self) -> List[Vertex]:
        return self._vertices

    @property
    def edges(self) -> List[Edge]:
        return self._edges


if __name__ == "__main__":
    import sys

    def print_usage():
        print(f"Использование: {sys.argv[0]} [ПУТЬ_ДО_ФАЙЛА_С_ГРАФОМ] [РЕЖИМ]")
        print(
            "Режимы:\n"
            "\texample - загружает граф и выводит его компоненты и матрицу смежности\n"
            "\ttask - решает задачу из вариант"
        )

    if len(sys.argv) < 3:
        print_usage()
        exit(-1)

    filename, mode, *_ = sys.argv[1:]

    graph = Graph()
    try:
        graph.load(filename)
    except Exception as e:
        print(e)
        exit(-1)

    match mode:
        case "example":
            print("Ребра графа:\n" + "\n".join(str(e) for e in graph.edges))
            print("Вершины графа:\n" + "\n".join(str(v) for v in graph.vertices))
            print("Матрица смежности:\n" + "\n".join(str(row) for row in graph.to_adj_matrix()))
        case "task":
            pass  # TASK_EXECUTION

        case _:
            print_usage()
            exit(-1)
