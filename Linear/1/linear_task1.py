import random
import time


# класс Node - узел дека
class Node:
    def __init__(self, next=None, prev=None, elem=None):
        # ссылка на следующий элемент
        self.next = next
        # ссылка на предыдущий элемент
        self.prev = prev
        # ссылка на самого себя
        self.elem = elem


# класс DoubleLinkedList - дек
class DoubleLinkedList:
    def __init__(self, head=None, tail=None, length=0):
        # количество операций
        self.n_op = 0

        # ссылка на голову
        self.head = head
        self.n_op += 1
        # ссылка на хвост
        self.tail = tail
        self.n_op += 1
        # длина дека
        self.length = length
        self.n_op += 1

    # добавление элемента в конец дека
    def push_right(self, elem):

        # проверка на добавление первого элемента в конец, если таковых не имеется
        if self.tail is None:  # length == 0

            self.n_op += 1
            # добавление узла
            new_node = Node(None, None, elem)
            self.n_op += 4
            # т.к элементов еще нет, голова будет присвоена нынешнему узлу
            self.head = new_node
            self.n_op += 1
            # т.к элементов еще нет, хвост будет равен голове
            self.tail = self.head
            self.n_op += 1
            # т.к в деке только один элемент, то длина всего дека равна 1
            self.length = 1
            self.n_op += 1
        # в ином случае, если хотя бы 1 элемент присутствует
        else:
            self.n_op += 1
            # добавление узла
            new_node = Node(None, self.tail, elem)
            self.n_op += 4
            # т.к был создан новый узел, хвост будет являться нынешним узлом
            self.tail.next = new_node
            self.n_op += 1
            # глобальная ссылка на хвост  также будет указывать на новый узел
            self.tail = new_node
            self.n_op += 1
            # т.к был создан новый узел, длина увеличивается на 1
            self.length += 1
            self.n_op += 2

    # удаление элемента из конца дека
    def pop_right(self):
        # проверка на наличие хотя бы 1 элемента, для удаления
        if self.tail is None:  # length == 0
            self.n_op += 1
            raise Exception("Нечего удалять")
        # если элемент в деке только 1
        elif self.length == 1:
            self.n_op += 1
            # ссылки на хвост больше нет
            self.tail = None
            self.n_op += 1
            # ссылки на голову больше нет
            self.head = None
            self.n_op += 1
            # длина уменьшается на 1
            self.length -= 1
            self.n_op += 2
        # иначе, если элементов в деке больше 1
        else:
            self.n_op += 1
            # ссылка на хвост, будет указывать на предыдущий элемент,после самого последнего, который мы удалим
            self.tail = self.tail.prev
            self.n_op += 1
            # если ссылка на хвост существует
            if self.tail is not None:
                self.n_op += 1
                # ссылки у последнего элемента на следующий нет
                self.tail.next = None
                self.n_op += 1
            # т.к был удален узел, длина уменьшается на 1
            self.length -= 1
            self.n_op += 2

    # добавление элемента в начало дека
    def push_left(self, elem):
        # проверка на добавление первого элемента в начало, если таковых не имеется
        if self.head is None:
            self.n_op += 1
            # добавление узла
            new_node = Node(None, None, elem)
            self.n_op += 4
            # т.к элементов еще нет, голова будет присвоена нынешнему узлу
            self.head = new_node
            self.n_op += 1
            # т.к элементов еще нет, хвост будет равен голове
            self.tail = self.head
            self.n_op += 1
            # т.к в деке только один элемент, то длина всего дека равна 1
            self.length = 1
            self.n_op += 1
        # в ином случае, если хотя бы 1 элемент присутствует
        else:
            self.n_op += 1
            # добавление узла
            new_node = Node(self.head, None, elem)
            self.n_op += 4
            # т.к был создан новый узел, голова будет являться нынешним узлом
            self.head.prev = new_node
            self.n_op += 1
            # глобальная ссылка на голову  также будет указывать на новый узел
            self.head = self.head.prev
            self.n_op += 1
            # т.к был создан новый узел, длина увеличивается на 1
            self.length += 1
            self.n_op += 2

    # удаление элемента из начала дека
    def pop_left(self):
        # проверка на наличие хотя бы 1 элемента, для удаления
        if self.head is None:  # length == 0
            self.n_op += 1
            raise Exception("Нечего удалять")
        # если элемент в деке только 1
        elif self.length == 1:
            self.n_op += 1
            # ссылки на хвост больше нет
            self.tail = None
            self.n_op += 1
            # ссылки на голову больше нет
            self.head = None
            self.n_op += 1
            # длина уменьшается на 1
            self.length -= 1
            self.n_op += 2
        # иначе, если элементов в деке больше 1
        else:
            self.n_op += 1
            # ссылка на голову, будет указывать на следующий элемент, после самого первого, который мы удалим
            self.head = self.head.next
            self.n_op += 1
            # если ссылка но голову существует
            if self.head is not None:
                self.n_op += 1
                # ссылки у первого элемента на предыдущий нет
                self.head.prev = None
                self.n_op += 1
            # т.к был удален узел, длина уменьшается на 1
            self.length -= 1
            self.n_op += 2

    # получение элемента из любого узла дека
    def get(self, index):
        buff = DoubleLinkedList()
        gotten_elem = None
        while self.length >= index:
            # если индекс дека равен длине
            if self.length == index:
                gotten_elem = self.right_elem()

            # получение самого последнего элемента дека
            right_elem = self.right_elem()
            # добавление этого элемента слева в буфер
            buff.push_left(right_elem)
            # удаление последнего узла из дека
            self.pop_right()

        # [выгрузка элементов из буфера обратно в дек]
        # пока длина буфера не равна 0
        while buff.length != 0:
            # получение самого первого элемента буфера
            left_elem = buff.left_elem()
            # добавление этого элемента справа обратно в дек
            self.push_right(left_elem)
            # удаление первого узла из буфера
            buff.pop_left()

        return gotten_elem

    # установка элемента в любой узел дека
    def set(self, index, new_elem):
        buff = DoubleLinkedList()
        while self.length >= index:
            # если индекс дека равен длине
            if self.length == index:
                self.pop_right()
                self.push_right(new_elem)

            # получение самого последнего элемента дека
            right_elem = self.right_elem()
            # добавление этого элемента слева в буфер
            buff.push_left(right_elem)
            # удаление последнего узла из дека
            self.pop_right()

        # [выгрузка элементов из буфера обратно в дек]
        # пока длина буфера не равна 0
        while buff.length != 0:
            # получение самого первого элемента буфера
            left_elem = buff.left_elem()
            # добавление этого элемента справа обратно в дек
            self.push_right(left_elem)
            # удаление первого узла из буфера
            buff.pop_left()

    # возвращение длины списка
    def len(self):
        self.n_op += 1
        return self.length

    # возвращение самого первого элемента
    def left_elem(self):
        self.n_op += 1
        return self.head.elem

    # возвращение самого последнего элемента
    def right_elem(self):
        self.n_op += 1
        return self.tail.elem

    # возвращение количества операций
    def num_of_operations(self):
        return self.n_op

    # вывод всех элементов дека
    def print_list(self):
        # получение ссылки на голову
        current = self.head
        # пока узел существует
        while current:
            # печатается его элемент
            print(current.elem)
            # получение ссылки на следующий узел
            current = current.next


# поиск максимального элемента в деке
def max(dll):
    # присвоение отрицательного значения для последующего поиска максимального значения
    max_elem = -1
    dll.n_op += 1
    # инициализация буфера для отгрузки элементов из дека
    buff = DoubleLinkedList()
    dll.n_op += 4

    # [поиск максимума]
    # пока длина дека не равна 0
    while dll.length != 0:
        dll.n_op += 1
        # получение самого последнего элемента дека
        right_elem = dll.right_elem()
        dll.n_op += 2

        # добавление этого элемента слева в буфер
        buff.push_left(right_elem)
        dll.n_op += 2
        # удаление последнего узла из дека
        dll.pop_right()
        dll.n_op += 1

        # если последний элемент дека больше максимального
        if right_elem > max_elem:
            dll.n_op += 1
            # максимальный элемент становится новым найденным
            max_elem = right_elem
            dll.n_op += 1

    # [выгрузка элементов из буфера обратно в дек]
    # пока длина буфера не равна 0
    while buff.length != 0:
        dll.n_op += 1
        # получение самого последнего элемента буфера
        right_elem = buff.right_elem()
        dll.n_op += 2
        # добавление этого элемента слева обратно в дек
        dll.push_left(right_elem)
        dll.n_op += 2
        # удаление последнего узла из буфера
        buff.pop_right()
        dll.n_op += 1

    # возврат максимального элемента
    return max_elem
    dll.n_op += 1


# сортировка дека сравнением и подсчетом
def counting_sort(dll):

    # инициализация буфера для подсчета и сохранения элементов (буфер заполняется нулями от 0 до максимального элемента + 1)
    counting_buff = [0 for i in range(max_elem + 1)]
    dll.n_op += 1

    # инициализация буфера для отгрузки элементов из дека
    buff = DoubleLinkedList()
    dll.n_op += 4

    # [сохранение элементов дека в буфер подсчета для сортировки]
    # пока длина дека не равна 0
    while dll.length != 0:
        dll.n_op += 1
        # получение самого последнего элемента дека
        right_elem = dll.right_elem()
        dll.n_op += 2
        # сохранение и подсчет элементов в качестве индексов буфера подсчета
        counting_buff[right_elem] += 1
        dll.n_op += 3
        # добавление этого элемента слева в буфер
        buff.push_left(right_elem)
        dll.n_op += 2
        # удаление последнего узла из дека
        dll.pop_right()
        dll.n_op += 1

    # пока длина буфера не равна 0
    while buff.length != 0:
        dll.n_op += 1
        # получение самого последнего элемента буфера
        right_elem = buff.right_elem()
        dll.n_op += 2
        # добавление этого элемента слева обратно в дек
        dll.push_left(right_elem)
        dll.n_op += 2
        # удаление последнего узла из буфера
        buff.pop_right()
        dll.n_op += 1

    # итерация от 0 до максимального элемента + 1 (максимальный элемент + 1,тк важно, чтобы итерация доходила до индекса максимального элемента)
    for i in range(max_elem + 1):
        dll.n_op += 1
        # итерация от 0 до количества повторений элемента, который является индексом
        for j in range(counting_buff[i]):  # сколько раз потвторяется
            dll.n_op += 1
            # удаление первого узла из дека
            dll.pop_left()
            dll.n_op += 1
            # добавление нового узла в дек справа
            dll.push_right(i)
            dll.n_op += 2


# заполнение дека рандомными целыми числами
def random_filling(elem_count):
    # итерация от 0 до нужного количества
    for i in range(elem_count):
        # добавление нового узла в дек справа с элементом в диапазоне от 1 до 1000
        dll.push_right(random.randint(1, 1000))


elem_count = 10000

count = 0

for i in range(10):
    count += elem_count

    # инициализация дека
    dll = DoubleLinkedList()

    # вызов метода для рандомного заполнения дека
    random_filling(count)

    # начало отсчета сортировки
    start_time = time.time()

    # вызов метода для поиска максимального элемента в деке
    max_elem = max(dll)
    dll.n_op += 3

    # сортировка дека
    counting_sort(dll)
    dll.n_op += 2
    # dll.print_list()

    this_time = round(time.time() - start_time, 3)
    # конец отсчета сортировки и последующий вывод количества элементов, затраченного времени и числа операций
    print(
        f"{i}) Count of elements: {dll.length};   Total time: {this_time} sec;   Num of operations: {dll.num_of_operations()};"
    )
