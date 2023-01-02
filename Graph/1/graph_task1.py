import itertools

import matplotlib.pyplot as plt
import networkx as nx


# Класс TextColors - класс с escape - последовательностями ANSI
# для цветового оформления вывода
class TextColors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# Класс Graph - Граф
class Graph:
    def __init__(self):
        self.length = 0
        self.vertex_names = {}
        self.all_cycles_buff = []
        self.visual_buff = []
        self.matrix = [[0 for x in range(self.length)] for y in range(self.length)]

    # Визуализация графа
    def visualize(self):
        G = nx.DiGraph()
        G.add_edges_from(self.visual_buff)
        nx.draw_networkx(G)
        plt.show()

    # Добавление вершины с индеком в граф
    def add_vertex_with_index(self, v_name, v_index):

        if (not v_name in self.vertex_names) and (not v_index in self.vertex_names.values()):
            self.vertex_names[v_name] = v_index

            if v_index >= self.length:

                self.length = v_index + 1

                new_matrix = [[0 for x in range(self.length)] for y in range(self.length)]

                for i in range(len(self.matrix)):
                    for j in range(len(self.matrix)):
                        new_matrix[i][j] = self.matrix[i][j]

                self.matrix = new_matrix
        elif v_name in self.vertex_names:
            print(
                f"{TextColors.FAIL}///ERROR///{TextColors.ENDC} ВЕРШИНА С НАЗВАНИЕМ '{v_name}' УЖЕ ИСПОЛЬЗУЕТСЯ!"
            )
        else:
            print(f"{TextColors.FAIL}///ERROR///{TextColors.ENDC} ИНДЕКС '{v_index}' УЖЕ ИСПОЛЬЗУЕТСЯ!")

    # Добавление вершины в граф (индекс выбирается автоматически)
    def add_vertex(self, v_name):

        if not v_name in self.vertex_names:
            self.vertex_names[v_name] = self.length

            self.length += 1

            new_matrix = [[0 for x in range(self.length)] for y in range(self.length)]

            for i in range(len(self.matrix)):
                for j in range(len(self.matrix)):
                    new_matrix[i][j] = self.matrix[i][j]

            self.matrix = new_matrix
        else:
            print(
                f"{TextColors.FAIL}///ERROR///{TextColors.ENDC} ВЕРШИНА С НАЗВАНИЕМ '{v_name}' УЖЕ ИСПОЛЬЗУЕТСЯ!"
            )

    # Удаление вершины из графа
    def del_vertex(self, v_name):

        if v_name in self.vertex_names:
            v_index = self.vertex_names[v_name]
            self.vertex_names.pop(v_name)

            # Удаление всех дуг, связанных с удаленной вершиной
            for i in range(self.length):
                for j in range(self.length):
                    if i == v_index or j == v_index:
                        if self.matrix[i][j] == 1:
                            self.matrix[i][j] = 0

        else:
            print(f"{TextColors.FAIL}///ERROR///{TextColors.ENDC} НЕТ ВЕРШИНЫ С НАЗВАНИЕМ '{v_name}'!")

    ##обавление ребра в граф
    def add_edge(self, v1_name, v2_name):
        if v1_name and v2_name in self.vertex_names:

            v1_index = self.vertex_names[v1_name]
            v2_index = self.vertex_names[v2_name]

            self.matrix[v1_index][v2_index] = 1

            self.visual_buff.append([v1_name, v2_name])

        elif v1_name not in self.vertex_names:
            print(f"{TextColors.FAIL}///ERROR///{TextColors.ENDC} НЕТ ВЕРШИНЫ С НАЗВАНИЕМ '{v1_name}'!")
        elif v2_name not in self.vertex_names:
            print(f"{TextColors.FAIL}///ERROR///{TextColors.ENDC} НЕТ ВЕРШИНЫ С НАЗВАНИЕМ '{v2_name}'!")
        else:
            print(
                f"{TextColors.FAIL}///ERROR///{TextColors.ENDC} НЕТ ВЕРШИН С НАЗВАНИЯМИ '{v1_name}' и '{v2_name}'!"
            )

    # Удаление ребра из графа
    def del_edge(self, v1_name, v2_name):
        if v1_name and v2_name in self.vertex_names:

            v1_index = self.vertex_names[v1_name]
            v2_index = self.vertex_names[v2_name]

            self.matrix[v1_index][v2_index] = 0

            self.visual_buff.remove([v1_name, v2_name])

        elif v1_name not in self.vertex_names:
            print(f"{TextColors.FAIL}///ERROR///{TextColors.ENDC} НЕТ ВЕРШИНЫ С НАЗВАНИЕМ '{v1_name}'!")
        elif v2_name not in self.vertex_names:
            print(f"{TextColors.FAIL}///ERROR///{TextColors.ENDC} НЕТ ВЕРШИНЫ С НАЗВАНИЕМ '{v2_name}'!")
        else:
            print(
                f"{TextColors.FAIL}///ERROR///{TextColors.ENDC} НЕТ ВЕРШИН С НАЗВАНИЯМИ '{v1_name}' и '{v2_name}'!"
            )

    # Получение первого индекса, смежного с выранным
    def get_first_vertex(self, v_index):
        for j in range(self.length):
            if self.matrix[v_index][j] == 1:

                return j

    # Получение первого индекса, смежного с вершиной v_index, но после next_v_index
    def get_next_vert(self, v_index, next_v_index):
        for j in range(self.length):
            if self.matrix[v_index][j] == 1 and j > next_v_index:

                return j

    # Изменить индекс вершины
    def change_vertex_index(self, v_name, new_v_index):
        if (v_name in self.vertex_names) and (not new_v_index in self.vertex_names.values()):
            old_v_index = self.vertex_names[v_name]
            self.vertex_names[v_name] = new_v_index

            if new_v_index >= self.length:
                self.length = new_v_index + 1

                new_matrix = [[0 for x in range(self.length)] for y in range(self.length)]

                for i in range(len(self.matrix)):
                    for j in range(len(self.matrix)):
                        new_matrix[i][j] = self.matrix[i][j]

                self.matrix = new_matrix

            for i in range(len(self.matrix)):
                for j in range(len(self.matrix)):

                    if self.matrix[old_v_index][j] == 1:
                        self.matrix[old_v_index][j] = 0
                        self.matrix[new_v_index][j] = 1

                    if self.matrix[j][old_v_index] == 1:
                        self.matrix[j][old_v_index] = 0
                        self.matrix[j][new_v_index] = 1
        elif not v_name in self.vertex_names:
            print(f"{TextColors.FAIL}///ERROR///{TextColors.ENDC} НЕТ ВЕРШИНЫ С НАЗВАНИЕМ '{new_v_index}'!")
        else:
            print(f"{TextColors.FAIL}///ERROR///{TextColors.ENDC} ИНДЕКС '{new_v_index}' УЖЕ ИСПОЛЬЗУЕТСЯ!")

    # Вывести матрицу смежности
    def print_matrix(self):
        for line in self.matrix:
            print(line)

    # Получение последних элементов маршрутов буфера (для работы алгоритма)
    def last_in_buff(self, buff):
        last_el_buff = []
        try:
            for i in range(len(buff)):

                z = buff[i][len(buff[i]) - 1][1]  # [len(buff[i][len(buff[i])-1]
                last_el_buff.append(z)

        except:
            last_el_buff.append(buff[0][1])

        last_el_buff = list(set(last_el_buff))

        return last_el_buff

    # Алгоритм нахождения циклов (проходит по всем маршрутам и хранит их)
    def search_cycles_algorithm(self, start_i, start_j):

        buff = [[(start_i, start_j)]]

        # start_time = time.time()
        for c in range(self.length):

            for i in range(self.length):

                last_el_buff = self.last_in_buff(buff)
                for j in range(self.length):

                    for k in range(len(last_el_buff)):

                        if self.matrix[i][j] == 1 and (i == last_el_buff[k]):

                            for l in range(len(buff)):

                                if buff[l][len(buff[l]) - 1][1] == last_el_buff[k]:
                                    temp = []
                                    for elem in buff[l]:
                                        temp.append(elem)

                                    temp.append((i, j))
                                    buff.append(temp)

            buff.sort()
            buff = list(num for num, _ in itertools.groupby(buff))

        final_buff = []
        for i in range(len(buff)):
            if buff[i][0][0] == buff[i][len(buff[i]) - 1][1]:
                if len(set(buff[i])) == len(buff[i]):
                    final_buff.append(buff[i])

        temp = []
        for i in range(len(final_buff)):
            tmp_dct = {}
            for j in range(len(final_buff[i])):
                for k in range(2):
                    if not final_buff[i][j][k] in tmp_dct:
                        tmp_dct[final_buff[i][j][k]] = 1
                    else:
                        tmp_dct[final_buff[i][j][k]] += 1

            for key in tmp_dct:
                if tmp_dct[key] > 2:
                    temp.append(i)
                    break

        for i in range(len(temp)):
            final_buff.pop(temp[i])

            for j in range(len(temp)):
                temp[j] -= 1

        # print(f"\n{TextColors.OKGREEN}///DEBUG///{TextColors.ENDC} FOR EDGE {start_i,start_j}:")
        # for i in final_buff:
        #     print(i)

        # print(f"{TextColors.OKGREEN}///DEBUG///{TextColors.ENDC} ELAPSED TIME: {time.time()-start_time} sec")

        return final_buff

    # Сохранение циклов
    def collect_cycles(self, start_i, start_j):

        self.all_cycles_buff += self.search_cycles_algorithm(start_i, start_j)

    # Вывод циклов в виде индексов (для дебаггинга)
    def print_cycles_indexes(self):
        print(f"\n{TextColors.OKGREEN}///DEBUG///{TextColors.ENDC} ЦИКЛЫ:")

        # for cycle in self.all_cycles_buff:
        #     print(cycle)

        for cycle_list in self.all_cycles_buff:
            cycle = str()
            for elem in cycle_list:
                cycle += str(elem[0]) + "->"
            cycle += str(cycle_list[len(cycle_list) - 1][1])
            print(cycle)

    # Вывод циклов
    def print_cycles(self, cycle_length=None):

        original_lists = []
        for cycle_list in self.all_cycles_buff:
            cycle = str()

            if cycle_length == None:
                self.cleared_cycles(cycle_list, cycle, original_lists)
            else:
                if cycle_length == len(cycle_list):
                    self.cleared_cycles(cycle_list, cycle, original_lists)

        self.all_cycles_buff = []

    # Очистка повторяющихся циклов их вывод
    def cleared_cycles(self, cycle_list, cycle, original_lists):
        temp_cycle_list = []
        for elem in cycle_list:
            cycle += list(self.vertex_names.keys())[list(self.vertex_names.values()).index(elem[0])] + "->"
            temp_cycle_list.append(elem[0])
        cycle += list(self.vertex_names.keys())[
            list(self.vertex_names.values()).index(cycle_list[len(cycle_list) - 1][1])
        ]

        in_original_lists = False
        for elem in original_lists:
            if set(temp_cycle_list) != set(elem):
                continue
            else:
                in_original_lists = True
                break
        if in_original_lists == False:
            original_lists.append(temp_cycle_list)
            print(cycle)

    # Поиск циклов
    def find_all_cycles(self, cycle_length=None):
        for i in range(self.length):
            for j in range(self.length):
                if self.matrix[i][j] == 1:
                    self.collect_cycles(i, j)

        if cycle_length == None:
            print(f"\n{TextColors.OKGREEN}///OUTPUT///{TextColors.ENDC} ВСЕ ЦИКЛЫ:")
        else:
            print(
                f"\n{TextColors.OKGREEN}///OUTPUT///{TextColors.ENDC} ЦИКЛЫ ДЛИНОЙ, РАВНОЙ {TextColors.OKBLUE}{cycle_length}{TextColors.ENDC}:"
            )
        self.print_cycles(cycle_length)

    # Поиск циклов из ребра
    def find_cycles_from_edge(self, v1_name, v2_name, cycle_length=None):
        if v1_name and v2_name in self.vertex_names:

            v1_index = self.vertex_names[v1_name]
            v2_index = self.vertex_names[v2_name]
            self.collect_cycles(v1_index, v2_index)

            if cycle_length == None:
                print(
                    f"\n{TextColors.OKGREEN}///OUTPUT///{TextColors.ENDC} ЦИКЛЫ ИЗ РЕБРА ['{v1_name}'->'{v2_name}']:"
                )
            else:
                print(
                    f"\n{TextColors.OKGREEN}///OUTPUT///{TextColors.ENDC} ЦИКЛЫ ИЗ РЕБРА ['{v1_name}'->'{v2_name}'] ДЛИНОЙ, РАВНОЙ {TextColors.OKBLUE}{cycle_length}{TextColors.ENDC}:"
                )
            self.print_cycles(cycle_length)

        elif v1_name not in self.vertex_names:
            print(f"{TextColors.FAIL}///ERROR///{TextColors.ENDC} НЕТ ВЕРШИНЫ С НАЗВАНИЕМ '{v1_name}'!")
        elif v2_name not in self.vertex_names:
            print(f"{TextColors.FAIL}///ERROR///{TextColors.ENDC} НЕТ ВЕРШИНЫ С НАЗВАНИЕМ '{v2_name}'!")
        else:
            print(
                f"{TextColors.FAIL}///ERROR///{TextColors.ENDC} НЕТ ВЕРШИН С НАЗВАНИЯМИ '{v1_name}' и '{v2_name}'!"
            )

    # Поиск циклов из вершины
    def find_cycles_from_vertex(self, v_name, cycle_length=None):
        if v_name in self.vertex_names:
            v_index = self.vertex_names[v_name]
            for j in range(self.length):
                if self.matrix[v_index][j] == 1:
                    self.collect_cycles(v_index, j)

            if cycle_length == None:
                print(f"\n{TextColors.OKGREEN}///OUTPUT///{TextColors.ENDC} ЦИКЛЫ ИЗ ВЕРШИНЫ '{v_name}:")
            else:
                print(
                    f"\n{TextColors.OKGREEN}///OUTPUT///{TextColors.ENDC} ЦИКЛЫ ИЗ ВЕРШИНЫ '{v_name}' ДЛИНОЙ, РАВНОЙ {TextColors.OKBLUE}{cycle_length}{TextColors.ENDC}:"
                )
            self.print_cycles(cycle_length)

        else:
            print(f"{TextColors.FAIL}///ERROR///{TextColors.ENDC} НЕТ ВЕРШИНЫ С НАЗВАНИЕМ '{v_name}'!")


graph = Graph()

graph.add_vertex("A")
graph.add_vertex("B")
graph.add_vertex("C")
graph.add_vertex("D")
graph.add_vertex("E")
graph.add_vertex("F")
graph.add_vertex("G")


graph.add_edge("A", "B")
graph.add_edge("B", "C")
graph.add_edge("C", "D")
graph.add_edge("D", "A")
graph.add_edge("B", "D")
graph.add_edge("A", "G")
graph.add_edge("G", "D")
graph.add_edge("C", "E")
graph.add_edge("E", "B")
graph.add_edge("E", "F")
graph.add_edge("F", "B")
graph.add_edge("F", "A")


graph.find_cycles_from_vertex("C", cycle_length=3)
graph.find_cycles_from_vertex("C")

graph.find_cycles_from_edge("G", "D", cycle_length=2)
graph.find_cycles_from_edge("G", "D")

graph.find_all_cycles(cycle_length=3)
graph.find_all_cycles()

graph.visualize()
