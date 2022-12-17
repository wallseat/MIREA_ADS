import os
import re
from enum import Enum
from pathlib import Path
from re import Match
from typing import Optional


class TaskType(int, Enum):
    LINEAR = 1
    TREE = 2
    GRAPH = 3

    def get_base_path(self) -> Path:
        return Path(self.name.lower().capitalize())

    def get_task_prefix(self) -> str:
        return self.name.lower()


class LinearStructType(int, Enum):
    STACK_ARRAY = 1
    STACK_LIB = 2
    STACK_POINTERS = 3
    QUEUE_ARRAY = 4
    QUEUE_LIB = 5
    QUEUE_POINTERS_HEAD = 6
    QUEUE_POINTERS_HEAD_TAIL = 7
    DEQUE_POINTERS = 8

    def get_abc_path(self) -> Path:
        return (
            Path("abc") / self.name.lower().split("_")[0] / (self.name.lower() + ".py")
        )


def get_task_num() -> int:
    task_num = input("Введите номер варианта: ")
    if not task_num.isdigit():
        print("Введенный номер варианта не является числом!")
        exit(-1)

    return int(task_num)


def get_task_type() -> TaskType:
    task_type = input(
        "Тип задания:\n" "* Линейные - 1\n" "* Деревья - 2\n" "* Графы - 3\n"
    )

    try:
        task_type = TaskType(int(task_type))
    except Exception:
        print("Неверный тип задания!")
        exit(-1)

    return task_type


def get_linear_struct_type() -> LinearStructType:
    struct_type = input(
        "Введите тип линейной структуры:\n"
        "* Стек (массив) - 1\n"
        "* Стек (библиотека классов) - 2\n"
        "* Стек (указатели) - 3\n"
        "* Очередь (массив) - 4\n"
        "* Очередь (библиотека классов) - 5\n"
        "* Очередь (указатели, голова) - 6\n"
        "* Очередь (указатели, голова-хвост) - 7\n"
        "* Дек (указатели) - 8\n"
    )

    try:
        struct_type = LinearStructType(int(struct_type))
    except Exception:
        print("Неверный тип структуры!")
        exit(-1)

    return struct_type


def read_abc_file(path: Path) -> str:
    lines = path.read_text().splitlines()
    end_of_abc = -1

    for i, line in enumerate(lines):
        if line.startswith('if __name__ == "__main__":'):
            end_of_abc = i
            break

    return "\n".join(lines[:end_of_abc])


def create_task_file(task_type: TaskType, task_num: int) -> Path:
    task_dir = task_type.get_base_path() / str(task_num)
    task_dir.mkdir(parents=True)

    task_py_file = task_dir / f"{task_type.get_task_prefix()}_task{task_num}.py"
    task_py_file.touch()

    return task_py_file


def create_linear_task(task_num: int, struct_type: LinearStructType) -> None:
    task_type = TaskType.LINEAR

    task_py_file = create_task_file(task_type, task_num)

    struct_abc = task_type.get_base_path() / struct_type.get_abc_path()
    struct_abc_data = read_abc_file(struct_abc)

    with task_py_file.open("w") as f:
        f.write(struct_abc_data)
        f.write("\n")
        f.write(
            (task_type.get_base_path() / "abc" / "task_runner.py.template").read_text()
        )


def create_graph_task(task_num: int) -> None:
    task_type = TaskType.GRAPH

    task_py_file = create_task_file(task_type, task_num)

    graph_abc = task_type.get_base_path() / "graph.py"

    task_py_file.write_text(graph_abc.read_text())


def open_task(task_dir_path: Path) -> None:
    task_py_file: Optional[Match] = None
    for file in task_dir_path.iterdir():
        task_py_file = re.match(r"\w+_task[0-9]+.py", file.name) or task_py_file

    if task_py_file:
        os.system(f"code -r {task_dir_path / task_py_file.string} ")
    else:
        os.system(f"code -r {task_dir_path}")


def main():
    task_num = get_task_num()
    task_type = get_task_type()

    path = task_type.get_base_path() / str(task_num)

    if path.exists():
        print("Задание с таким номером варианта уже существует!")
        open_task(path)
        exit(-1)

    match task_type:
        case TaskType.LINEAR:

            struct_type = get_linear_struct_type()
            create_linear_task(task_num, struct_type)

        case task_type.TREE:
            raise NotImplemented()

        case task_type.GRAPH:
            create_graph_task(task_num)

    open_task(path)


if __name__ == "__main__":
    main()
