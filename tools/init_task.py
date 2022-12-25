import json
import os
import re
from enum import Enum
from pathlib import Path
from re import Match
from subprocess import getoutput
from typing import Optional

from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage
from PIL import Image, ImageDraw, ImageFont


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


def create_task_file(task_type: TaskType, task_num: int) -> Path:
    task_dir = task_type.get_base_path() / str(task_num)
    task_dir.mkdir(parents=True, exist_ok=True)

    task_py_file = task_dir / f"{task_type.get_task_prefix()}_task{task_num}.py"
    task_py_file.touch()

    return task_py_file


def create_task_report_file(task_type: TaskType, task_num: int) -> Path:
    task_dir = task_type.get_base_path() / str(task_num)
    task_dir.mkdir(parents=True, exist_ok=True)

    task_py_file = (
        task_dir / f"{task_type.get_task_prefix().capitalize()}_{task_num}.docx"
    )
    task_py_file.touch()

    return task_py_file


def create_execution_screenshot(task_py_file: Path) -> Path:
    exec_out = getoutput("python3 " + str(task_py_file))

    img = Image.new("RGB", (840, 105), (255, 255, 255))
    d1 = ImageDraw.Draw(img)

    font = ImageFont.truetype(Path("fonts/consolas.ttf").as_posix(), 16)
    d1.text((5, 5), exec_out, (0, 0, 0), font=font)

    out_img = task_py_file.parent / "task_out.png"
    img.save(out_img, "PNG")

    return out_img


def create_linear_task(task_num: int, struct_type: LinearStructType) -> None:
    task_type = TaskType.LINEAR

    def read_abc_file(path: Path) -> str:
        lines = path.read_text().splitlines()
        end_of_abc = -1

        for i, line in enumerate(lines):
            if line.startswith('if __name__ == "__main__":'):
                end_of_abc = i
                break

        return "\n".join(lines[:end_of_abc])

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


def create_tree_task(task_num: int) -> None:
    task_type = TaskType.TREE
    normalized_task_num = task_num - 1

    def read_abc_file(path: Path, slice_after: bool = False) -> str:
        lines = path.read_text().splitlines()
        end_of_abc = -1

        for i, line in enumerate(lines):
            if line.startswith('if __name__ == "__main__":'):
                end_of_abc = i
                break

        if slice_after:
            if end_of_abc == -1:
                end_of_abc = 0
            lines = lines[end_of_abc:]
        else:
            if end_of_abc != -1:
                lines = lines[:end_of_abc]

        return "\n".join(lines)

    tree_abc_folder = task_type.get_base_path() / "abc"

    # Вычисление кода дерева
    if normalized_task_num % 50 <= 19:  # Дерево двоичного поиска
        tree_folder = tree_abc_folder / "bst"
        tree_class_name = "BST"

        tree_report = DocxTemplate(tree_folder / "bst_report.docx")

        if normalized_task_num % 20 <= 4:  # Указатель (курсор) на родителя
            tree_code = read_abc_file(tree_folder / "parent_pointer_bst.py")
            tree_realization = "Указатель (курсор) на родителя"

        elif normalized_task_num % 20 <= 9:  # Список сыновей
            tree_code = read_abc_file(tree_folder / "child_list_bst.py")
            tree_realization = "Список сыновей"

        elif normalized_task_num % 20 <= 14:  # Левый сын, правый брат (указатели)
            tree_code = read_abc_file(tree_folder / "left_right_pointer_bst.py")
            tree_realization = "Левый сын, правый брат (указатели)"

        elif normalized_task_num % 20 <= 19:  # Левый сын, правый брат (таблица, массив)
            tree_code = read_abc_file(tree_folder / "left_right_table_bst.py")
            tree_realization = "Левый сын, правый брат (таблица, массив)"

    elif normalized_task_num % 50 <= 34:  # Рандомизированное дерево двоичного поиска
        tree_folder = tree_abc_folder / "randomized_bst"
        tree_class_name = "RandomizedBST"

        tree_report = DocxTemplate(tree_folder / "randomized_bst_report.docx")

        if (normalized_task_num - 20) % 15 <= 4:  # Список сыновей
            tree_code = read_abc_file(tree_folder / "child_list_randomized_bst.py")
            tree_realization = "Список сыновей"

        elif (normalized_task_num - 20) % 15 <= 9:  # Левый сын, правый брат (указатели)
            tree_code = read_abc_file(
                tree_folder / "left_right_pointer_randomized_bst.py"
            )
            tree_realization = "Левый сын, правый брат (указатели)"

        elif (
            normalized_task_num - 20
        ) % 15 <= 14:  # Левый сын, правый брат (таблица, массив)
            tree_code = read_abc_file(
                tree_folder / "left_right_table_randomized_bst.py"
            )
            tree_realization = "Левый сын, правый брат (таблица, массив)"

    elif normalized_task_num % 50 <= 49:  # AVL-дерево
        tree_class_name = "AVL_BST"
        tree_folder = tree_abc_folder / "avl_bst"

        tree_report = DocxTemplate(tree_folder / "avl_bst_report.docx")

        if (normalized_task_num - 35) % 15 <= 4:  # Список сыновей
            tree_code = read_abc_file(tree_folder / "child_list_avl_bst.py")
            tree_realization = "Список сыновей"

        elif (normalized_task_num - 35) % 15 <= 9:  # Левый сын, правый брат, указатели
            tree_code = read_abc_file(tree_folder / "left_right_pointer_avl_bst.py")
            tree_realization = "Левый сын, правый брат (указатели)"

        elif (normalized_task_num - 35) % 15 <= 14:  # Левый сын, правый брат, массив
            tree_code = read_abc_file(tree_folder / "left_right_table_avl_bst.py")
            tree_realization = "Левый сын, правый брат (таблица, массив)"

    # Вычисления файла с кодом операции
    if normalized_task_num % 50 < 35:
        operations_file_name = f"{(normalized_task_num % 5) + 1}.py"

    else:
        operations_file_name = f"c_{(normalized_task_num % 5) + 1}.py"

    tree_operation_code = read_abc_file(
        tree_abc_folder / "operations" / operations_file_name,
        slice_after=True,
    )
    # find #$ ... $# in text and get content between
    tree_operation_line = re.findall(r"#\$.*\$\#", tree_operation_code)[0]
    tree_operation_code = tree_operation_code.replace(tree_operation_line, "")
    tree_operation = tree_operation_line[2:-2]

    # Вычисление кода вывода дерева А
    tree_prints_seq = json.loads((tree_abc_folder / "prints.json").read_text())
    if tree_prints_seq[normalized_task_num]:
        tree_a_print_code = (
            r'print("Дерево А в прямом порядке:\n" + str(tree_a.traverse_preorder()))'
        )
        tree_a_print = "Прямой"
    else:
        tree_a_print_code = r'print("Дерево А в обратном порядке:\n" + str(tree_a.traverse_postorder()))'
        tree_a_print = "Обратный"

    # Составление итогового кода
    tree_operation_code = tree_operation_code.replace(
        "# $print_A$", tree_a_print_code
    ).replace("TREE__", tree_class_name)

    task_code = tree_code + "\n\n" + tree_operation_code

    # Запись кода в файл
    task_py_file = create_task_file(task_type, task_num)
    task_py_file.write_text(task_code)

    task_out_screenshot = create_execution_screenshot(task_py_file)

    task_report_file = create_task_report_file(task_type, task_num)
    tree_report.render(
        {
            "task_num": task_num,
            "tree_realization": tree_realization,
            "tree_operation": tree_operation,
            "tree_a_print": tree_a_print,
            "task_code": task_code,
            "task_out_screenshot": InlineImage(
                tree_report,
                image_descriptor=task_out_screenshot.as_posix(),
                height=Mm(15),
            ),
        }
    )
    tree_report.save(task_report_file)


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
            create_tree_task(task_num)

        case task_type.GRAPH:
            create_graph_task(task_num)

    open_task(path)


if __name__ == "__main__":
    main()
