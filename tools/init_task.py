import os
import re
from pathlib import Path
from re import Match
from shutil import rmtree
from typing import Optional

from utils.task_utils import (
    TaskType,
    create_graph_task,
    create_linear_task,
    create_tree_task,
)


def get_task_num() -> int:
    task_num = input("Введите номер варианта: ")
    if not task_num.isdigit():
        print("Введенный номер варианта не является числом!")
        exit(-1)

    return int(task_num)


def get_task_type() -> TaskType:
    task_type = input("Тип задания:\n" "* Линейные - 1\n" "* Деревья - 2\n" "* Графы - 3\n")

    try:
        task_type = TaskType(int(task_type))
    except Exception:
        print("Неверный тип задания!")
        exit(-1)

    return task_type


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
        rmtree(path)

    match task_type:
        case TaskType.LINEAR:
            create_linear_task(task_num)

        case TaskType.TREE:
            create_tree_task(task_num)

        case TaskType.GRAPH:
            create_graph_task(task_num)

    open_task(path)


if __name__ == "__main__":
    main()
