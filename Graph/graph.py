import json
from typing import Dict, List, Optional, Tuple

_T_ADJ_MATRIX = List[List[int]]
_T_PATH = List[int]


class Vertex:
    _index: int
    label: str

    def __init__(self, index: int, label: Optional[str] = ""):
        self._index = index
        self.label = label

    @property
    def index(self) -> int:
        return self._index

    def __repr__(self):
        return f"Vertex[i: {self._index}, label: {self.label}]"


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

    def _load_adj_matrix(self, data: List[List[int]], dim: int) -> None:
        self._init_vertices(dim)
        for i, vertex in enumerate(data):
            for j, edge_len in enumerate(vertex):
                if edge_len > 0:
                    self.add_e(i, j, edge_len)

    def _load_adj_list(self, data: List[List[int]], dim: int) -> None:
        self._init_vertices(dim)

        for i, adj in enumerate(data):
            for j in adj:
                self.add_e(i, j, 1)

    def _load_edge_list(self, data: List[List[int]], dim: int) -> None:
        self._init_vertices(dim)

        for edge in data:
            if len(edge) == 3:
                v1, v2, edge_len = edge
            else:
                v1, v2, edge_len = *edge, 1

            self.add_e(v1, v2, edge_len)

    def _load_inc_matrix(self, data: List[List[int]], dim: int) -> None:
        self._init_vertices(dim)

        transposed_data = list(zip(*data))  # транспонирование

        for edge in transposed_data:
            v1 = None
            v2 = None
            v1_v2_len = 0
            v2_v1_len = 0
            for j in range(dim):
                if edge[j] != 0 and v1 is None:
                    v1 = j
                    v1_v2_len = edge[j]
                elif edge[j] != 0 and v2 is None:
                    v2 = j
                    v2_v1_len = edge[j]
                    break

            if v1_v2_len > 0:
                self.add_e(v1, v2, v1_v2_len)

            if v2_v1_len > 0:
                self.add_e(v2, v1, v2_v1_len)

    def _load_labels(self, labels: Dict[str, str]) -> None:
        for index, label in labels.items():
            index = int(index)
            self._vertices[index].label = label

    def load(self, filename: str) -> None:
        with open(filename, "r", encoding="utf8") as f:
            graph_json: dict = json.load(f)

        _format = graph_json.get("format", None)
        if _format is None:
            raise Exception("Не указан формат для задания графа! Смотри документацию!")

        _dim: Optional[str] = graph_json.get("dim", None)
        if _dim is None or not isinstance(_dim, int):
            raise Exception("Не укаказан/верный размер графа! Смотри документацию!")

        _data: Optional[List[List[int]]] = graph_json.get("data", None)
        if _data is None:
            raise Exception("Не заданны данные для построения графа! Смотри документацию!")

        _labels: Optional[Dict[str, str]] = graph_json.get("labels", None)

        if _format == "adj_matrix":
            self._load_adj_matrix(_data, _dim)

        elif _format == "adj_list":
            self._load_adj_list(_data, _dim)

        elif _format == "edge_list":
            self._load_edge_list(_data, _dim)

        elif _format == "inc_matrix":
            self._load_inc_matrix(_data, _dim)

        else:
            raise Exception("Неизвестный формат задания графа! Смотри документацию!")

        if _labels:
            self._load_labels(_labels)

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

    def to_adj_matrix(self) -> _T_ADJ_MATRIX:
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
        print(f"Использование: {sys.argv[0]} <режим> [ИМЯ_ФАЙЛА]")
        print(
            "Режимы:\n"
            "\texample - загружает граф и выводит его компоненты и матрицу смежности\n"
            "\ttask - решает задачу из вариант"
        )

    if len(sys.argv) < 3:
        print_usage()
        exit(-1)

    mode, filename, *_ = sys.argv[1:]

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
            pass

        case _:
            print_usage()
            exit(-1)
