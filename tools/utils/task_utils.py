import json
import re
import shutil
from enum import Enum
from pathlib import Path
from subprocess import PIPE, Popen
from textwrap import indent
from typing import Dict, List

import matplotlib.pyplot as plt
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage
from PIL import Image, ImageDraw, ImageFont
from utils.linear_utils import (
    get_n_op,
    merge_collection_sort_code,
    prepare_collection,
    prepare_sort,
    prepare_task_runner_code,
)


class TaskType(int, Enum):
    LINEAR = 1
    TREE = 2
    GRAPH = 3

    def get_base_path(self) -> Path:
        return Path(self.name.lower().capitalize())

    def get_task_prefix(self) -> str:
        return self.name.lower()


def create_task_file(task_type: TaskType, task_num: int) -> Path:
    task_dir = task_type.get_base_path() / str(task_num)
    task_dir.mkdir(parents=True, exist_ok=True)

    task_py_file = task_dir / f"{task_type.get_task_prefix()}_task{task_num}.py"
    task_py_file.touch()

    return task_py_file


def create_task_report_file(task_type: TaskType, task_num: int) -> Path:
    task_dir = task_type.get_base_path() / str(task_num)
    task_dir.mkdir(parents=True, exist_ok=True)

    task_py_file = task_dir / f"{task_type.get_task_prefix().capitalize()}_{task_num}.docx"
    task_py_file.touch()

    return task_py_file


def get_exec_out(
    task_py_file: Path,
    args: List[str] = None,
    input_: List[str] = None,
    timeout: float = None,
) -> str:
    if not args:
        args = []

    proc = Popen(
        ["python3", task_py_file.as_posix(), *args],
        stdout=PIPE,
        stderr=PIPE,
        stdin=PIPE,
        text=True,
    )
    input_str = None
    if input_:
        input_str = "".join(map(lambda s: s + "\n", input_))

    try:
        out, err = proc.communicate(input=input_str, timeout=timeout)
    except TimeoutError as e:
        raise RuntimeError(
            "Превышено время выполнения программы. Возможно ожидался ввод.\n" + indent(str(e), "\t")
        )

    if err:
        raise RuntimeError(
            f"\n* Произошла ошибка при выполнении: {task_py_file}\n"
            f"|\tАргументы: {args}\n"
            f"|\tВходные данные: {input_}\n"
            "|\tОшибка:\n" + indent(err, "\t|\t")
        )

    return out.strip()


def create_execution_screenshot(
    folder: Path,
    exec_out: str,
    image_name: str = "task_out.png",
    font_size: int = 16,
) -> Path:
    font = ImageFont.truetype(Path("fonts/CascadiaMono.ttf").as_posix(), font_size)
    padding = font_size // 2

    width, height = font.getsize_multiline(exec_out)

    width += 2 * padding
    height += 2 * padding

    img = Image.new("RGB", (width, height), (255, 255, 255))
    d1 = ImageDraw.Draw(img)

    d1.text((padding, padding // 3 * 1), exec_out, (0, 0, 0), font=font)

    out_img = folder / image_name
    img.save(out_img, "PNG")

    return out_img


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


def create_linear_task(task_num: int) -> Path:
    task_type = TaskType.LINEAR
    normalized_task_num = task_num - 1

    linear_abc_folder = task_type.get_base_path() / "abc"
    task_runner_file = linear_abc_folder / "task_runner.py"

    collections_folder = linear_abc_folder / "collections"
    sorts_folder = linear_abc_folder / "sorts"
    sort_theory_folder = linear_abc_folder / "sort_theory"

    step = 100
    # Вычисление кода линейной структуры
    if normalized_task_num % 8 == 0:  # Указатели, дек
        collection_file = collections_folder / "dequeue_pointers.py"
        link_type = "Указатели"
        collection_type = "Дек"

    elif normalized_task_num % 8 == 1:  # Указатели, Очередь с головой и хвостом
        collection_file = collections_folder / "queue_pointers_head_tail.py"
        link_type = "Указатели"
        collection_type = "Очередь с головой и хвостом"

    elif normalized_task_num % 8 == 2:  # Указатели, Очередь с 1 головой
        collection_file = collections_folder / "queue_pointers_head.py"
        link_type = "Указатели"
        collection_type = "Очередь с 1 головой"
        step /= 2

    elif normalized_task_num % 8 == 3:  # Указатели, Стек
        collection_file = collections_folder / "stack_pointers.py"
        link_type = "Указатели"
        collection_type = "Стек"
        step /= 2

    elif normalized_task_num % 8 == 4:  # Массив, очередь
        collection_file = collections_folder / "queue_array.py"
        link_type = "Массив"
        collection_type = "Очередь"

    elif normalized_task_num % 8 == 5:  # Массив, стек
        collection_file = collections_folder / "stack_array.py"
        link_type = "Массив"
        collection_type = "Стек"

    elif normalized_task_num % 8 == 6:  # Библиотека классов, очередь
        collection_file = collections_folder / "queue_lib.py"
        link_type = "Библиотека классов"
        collection_type = "Очередь"

    elif normalized_task_num % 8 == 7:  # Библиотека классов, стек
        collection_file = collections_folder / "stack_lib.py"
        link_type = "Библиотека классов"
        collection_type = "Стек"

    # Вычисление кода сортировки
    if normalized_task_num < 8:  # Сравнение и подсчет
        sort_file = sorts_folder / "counting_sort.py"
        report_theory_template = sort_theory_folder / "counting_sort.docx"
        sort_name = "Сравнение и подсчет"
        step *= 1.5

    elif normalized_task_num < 16:  # Шелла
        sort_file = sorts_folder / "shell_sort.py"
        report_theory_template = sort_theory_folder / "shell_sort.docx"
        sort_name = "Шелла"
        step //= 2

    elif normalized_task_num < 24:  # Бинарная вставка
        sort_file = sorts_folder / "binary_insertion_sort.py"
        report_theory_template = sort_theory_folder / "binary_insertion_sort.docx"
        sort_name = "Бинарная вставка"
        step *= 1.5

    elif normalized_task_num < 32:  # Быстрая сортировка Хоару (без медианного (pivot) элемента)
        sort_file = sorts_folder / "quick_no_median_sort.py"
        report_theory_template = sort_theory_folder / "quick_sort.docx"
        sort_name = "Быстрая сортировка Хоару (без медианного (pivot) элемента)"
        step *= 1.5

    elif normalized_task_num < 40:  # Быстрая сортировка (с медианой)
        sort_file = sorts_folder / "quick_with_median_sort.py"
        report_theory_template = sort_theory_folder / "quick_sort.docx"
        sort_name = "Быстрая сортировка Хоару (с медианным (pivot) элементом)"
        step *= 1.5

    elif normalized_task_num < 48:  # Естественное двухпутевое слияние
        sort_file = sorts_folder / "natural_merge_sort.py"
        report_theory_template = sort_theory_folder / "merge_sort.docx"
        sort_name = "Естественное двухпутевое слияние"
        step *= 1.5

    elif normalized_task_num < 56:  # Пирамидальная сортировка
        sort_file = sorts_folder / "heap_sort.py"
        report_theory_template = sort_theory_folder / "heap_sort.docx"
        sort_name = "Пирамидальная сортировка"
        step //= 2

    elif normalized_task_num < 64:  # Простая вставка
        sort_file = sorts_folder / "simple_insertion_sort.py"
        report_theory_template = sort_theory_folder / "simple_insertion_sort.docx"
        sort_name = "Простая вставка"
        step //= 2

    elif normalized_task_num < 72:  # Простой выбор
        sort_file = sorts_folder / "selection_sort.py"
        report_theory_template = sort_theory_folder / "selection_sort.docx"
        sort_name = "Простой выбор"
        step //= 4

    elif normalized_task_num < 80:  # Пузырьковая
        sort_file = sorts_folder / "bubble_sort.py"
        report_theory_template = sort_theory_folder / "bubble_sort.docx"
        sort_name = "Пузырьковая"
        step //= 4

    elif normalized_task_num < 88:  # Распределяющий подсчет
        sort_file = sorts_folder / "distributive_counting_sort.py"
        report_theory_template = sort_theory_folder / "counting_sort.docx"
        sort_name = "Распределяющий подсчет"
        step *= 1.5

    elif normalized_task_num < 96:  # Фиксированное двухпутевое слияние
        sort_file = sorts_folder / "fixed_merge_sort.py"
        report_theory_template = sort_theory_folder / "merge_sort.docx"
        sort_name = "Фиксированное двухпутевое слияние"
        step *= 1.5

    elif normalized_task_num < 100:  # Пирамидальная сортировка
        sort_file = sorts_folder / "heap_sort.py"
        report_theory_template = sort_theory_folder / "heap_sort.docx"
        sort_name = "Пирамидальная сортировка"
        step //= 4

    collection = prepare_collection(collection_file)
    sort = prepare_sort(sort_file)

    code = merge_collection_sort_code(collection, sort)
    code += prepare_task_runner_code(collection, sort, task_runner_file, step=int(step))

    task_file = create_task_file(task_type, task_num)
    task_file.write_text(code)

    exec_example_out = get_exec_out(task_file, args=["example"])
    task_out_example = create_execution_screenshot(
        task_file.parent,
        exec_example_out,
        image_name="task_out_example.png",
        font_size=24,
    )

    exec_tests_out = get_exec_out(task_file, args=["tests"])
    task_out_tests = create_execution_screenshot(
        task_file.parent,
        exec_tests_out,
        image_name="task_out_tests.png",
    )

    tests_results = []
    cur_row = {}
    for line in exec_tests_out.splitlines():
        if line.startswith("------"):
            cur_row["f_n"], cur_row["o_f_n"] = get_n_op(sort, cur_row["n"])
            cur_row["c1"], cur_row["c2"], cur_row["c3"], cur_row["c4"] = (
                cur_row["f_n"] / cur_row["time"],
                cur_row["o_f_n"] / cur_row["time"],
                cur_row["f_n"] / cur_row["n_op"],
                cur_row["o_f_n"] / cur_row["n_op"],
            )
            tests_results.append(cur_row)
            cur_row = {}

        elif line.startswith("Elements count:"):
            cur_row["n"] = int(line.split(": ")[1])
        elif line.startswith("Total time:"):
            cur_row["time"] = float(line.split(": ")[1])
        elif line.startswith("N_OP:"):
            cur_row["n_op"] = int(line.split(": ")[1])

    report = DocxTemplate(linear_abc_folder / "linear_report.docx")
    report_theory_template_sd = report.new_subdoc(report_theory_template)

    context = {
        "task_num": task_num,
        "link_type": link_type,
        "collection_type": collection_type,
        "collection_name": collection.collection_class_name,
        "sort_name": sort_name,
        "sort_theory": report_theory_template_sd,
        "task_code": code,
        "sort_asymptotic": str(sort.sort_asymptotic).replace("**", "^"),
        "sort_bigO_asymptotic": str(sort.sort_bigO_asymptotic).replace("**", "^"),
        "tests_results": tests_results,
        "task_out_example": InlineImage(
            report,
            image_descriptor=task_out_example.as_posix(),
            width=Mm(150),
        ),
        "task_out_tests": InlineImage(
            report,
            image_descriptor=task_out_tests.as_posix(),
            height=Mm(140),
        ),
    }

    c_formulas = {
        "c1": "$C1=\\frac{f(n)}{t}$",
        "c2": "$C2=\\frac{O(f(n))}{t}$",
        "c3": "$C3=\\frac{f(n)}{N\_OP}$",
        "c4": "$C4=\\frac{O(f(n))}{N\_OP}$",
    }

    for coefficient in ["c1", "c2", "c3", "c4"]:
        fig, ax = plt.subplots(1, 1, figsize=(12, 5))
        ax.plot(
            [row["n"] for row in tests_results],
            [row[coefficient] for row in tests_results],
        )
        ax.set_title(c_formulas[coefficient], fontdict={"fontsize": 20})

        ax.ticklabel_format(style="plain", useOffset=False)
        fig.set_label(coefficient.upper())

        file = task_file.parent / f"{coefficient}.png"

        fig.savefig(file)
        plt.close(fig)

        context[coefficient] = InlineImage(
            report,
            image_descriptor=file.as_posix(),
            width=Mm(150),
        )

    task_report_file = create_task_report_file(task_type, task_num)
    report.render(context)
    report.save(task_report_file)

    return task_file.parent


def create_graph_task(task_num: int) -> Path:
    def read_task_solve(file_path: Path) -> str:
        lines = file_path.read_text().splitlines()
        start = 0
        end = 0

        for i, line in enumerate(lines):
            if "# START" in line:
                start = i + 1
                continue
            if "# END" in line:
                end = i
                break

        if start == 0 or end == 0:
            raise ValueError("Неправильный формат файла решения")

        return "\n".join(lines[start:end])

    task_type = TaskType.GRAPH
    normalized_task_num = task_num - 1

    graph_abc_folder = task_type.get_base_path() / "abc"
    graph_readme_file = task_type.get_base_path() / "README.md"

    graph_class_file = graph_abc_folder / "graph.py"
    graph_class_code = read_abc_file(graph_class_file)
    graph_runner_code = read_abc_file(graph_class_file, slice_after=True)

    # load all existing graph tasks
    task_path: Dict[int, Path] = {}
    for folder in (graph_abc_folder / "tasks").glob("*"):
        comps = folder.name.split("__")
        for comp in comps:
            if "-" in comp:
                task_from, task_to = map(int, comp.split("-"))
                for num in range(task_from, task_to + 1):
                    task_path[num] = folder
            else:
                task_path[int(comp)] = folder

    if task_num not in task_path:
        raise ValueError(f"Решение задачи для варианта {task_num} не было найдено")

    graph_definitions = {0: "adj_matrix", 1: "inc_matrix", 2: "adj_list", 3: "edge_list"}

    if normalized_task_num <= 39:
        graph_definition = graph_definitions[normalized_task_num % 4]

    elif 40 <= normalized_task_num <= 43:
        graph_definition = graph_definitions[(normalized_task_num - 40) % 2]

    elif 44 <= normalized_task_num <= 52:
        graph_definition = graph_definitions[(normalized_task_num - 44) % 4]

    elif 53 <= normalized_task_num <= 55:
        graph_definition = graph_definitions[0]

    elif 56 <= normalized_task_num <= 71:
        graph_definition = graph_definitions[(normalized_task_num - 56) % 4]

    elif normalized_task_num >= 72:
        match normalized_task_num:
            case 72 | 75 | 77 | 78 | 80 | 83 | 86 | 89 | 93 | 97:
                graph_definition = graph_definitions[0]
            case 73 | 74 | 76 | 79 | 81 | 84 | 87 | 90 | 94 | 98:
                graph_definition = graph_definitions[2]
            case 82 | 85 | 88 | 91 | 95 | 99:
                graph_definition = graph_definitions[1]
            case 92 | 96:
                graph_definition = graph_definitions[3]

    task_abc_folder = task_path[task_num]
    task_matrix_txt = task_abc_folder / "matrix.txt"
    task_graph_png = task_abc_folder / "graph.png"
    task_solve_file = task_abc_folder / "task.py"
    task_algo_file = task_abc_folder / "algo.txt"
    task_outer_file = task_abc_folder / "outer.txt"
    needed_files = [task_matrix_txt, task_graph_png, task_solve_file, task_algo_file, task_outer_file]

    if not all(
        map(
            lambda f: f.exists(),
            needed_files,
        )
    ):
        raise RuntimeError(
            f"Не найдены все необходимые файлы для варианта {task_num}\n"
            + "\n".join(
                [f.name + ": " + ("Найден" if f.exists() else "Не найден") for f in needed_files],
            )
        )

    task_py_file = create_task_file(task_type, task_num)

    # Создание файла описания графа по заданию
    matrix_converters = graph_abc_folder / "matrix_converters"
    definition_theories = graph_abc_folder / "definition_theory_template"
    match graph_definition:
        case "adj_matrix":
            matrix_converter = matrix_converters / "adj_m_to_adj_m.py"
            definition_theory = definition_theories / "adj_matrix.docx"
            graph_definition_type = "Матрица смежности"

        case "inc_matrix":
            matrix_converter = matrix_converters / "adj_m_to_inc_m.py"
            definition_theory = definition_theories / "inc_matrix.docx"
            graph_definition_type = "Матрица инцидентности"

        case "adj_list":
            matrix_converter = matrix_converters / "adj_m_to_adj_list.py"
            definition_theory = definition_theories / "adj_list.docx"
            graph_definition_type = "Список смежности"

        case "edge_list":
            matrix_converter = matrix_converters / "adj_m_to_edge_list.py"
            definition_theory = definition_theories / "edge_list.docx"
            graph_definition_type = "Список дуг"

    graph_definition_file = task_py_file.parent / "graph_definition.json"

    if err := get_exec_out(matrix_converter, args=[str(task_matrix_txt), str(graph_definition_file)]):
        raise RuntimeError(f"Ошибка при конвертации матрицы варианта {task_num}.\n{err}")

    shutil.copy(task_graph_png, task_py_file.parent / "graph.png")
    shutil.copy(graph_readme_file, task_py_file.parent / "README.md")

    # Формируем решение задачи
    task_solve_code = read_task_solve(task_solve_file)

    code = (
        graph_class_code
        + "\n"
        + task_solve_code
        + "\n"
        + graph_runner_code.replace("pass  # TASK_EXECUTION", "task(graph)")
    )

    task_py_file.write_text(code)

    task_inputs = []
    task_inputs_file = task_abc_folder / "task_exec_inputs.txt"
    if task_inputs_file.exists():
        task_inputs = task_inputs_file.read_text().splitlines()

    # генерируем скриншоты
    example_out_screenshot = create_execution_screenshot(
        task_py_file.parent,
        get_exec_out(task_py_file, args=[str(graph_definition_file), "example"]),
        "example_out.png",
    )

    execs_out = []
    if task_inputs:  # если есть входные данные, то запускаем задачу с ними
        for task_input in task_inputs:
            execs_out.append(
                get_exec_out(
                    task_py_file,
                    args=[str(graph_definition_file), "task"],
                    input_=task_input.split(),
                    timeout=10,
                )
            )
    else:  # иначе запускаем задачу без входных данных
        execs_out.append(
            get_exec_out(
                task_py_file,
                args=[str(graph_definition_file), "task"],
                timeout=10,
            )
        )

    task_out_screenshot = create_execution_screenshot(
        task_py_file.parent,
        "\n\n".join(execs_out),
        "task_out.png",
    )

    graph_report = DocxTemplate(graph_abc_folder / "graph_report.docx")
    definition_theory_sd = graph_report.new_subdoc(definition_theory)

    task_report_file = create_task_report_file(task_type, task_num)
    graph_report.render(
        {
            "task_num": task_num,
            "task_algo": task_algo_file.read_text(),
            "graph_definition_type": graph_definition_type,
            "definition_theory": definition_theory_sd,
            "task_code": code,
            "graph_png": InlineImage(
                graph_report,
                task_graph_png.as_posix(),
                width=Mm(70),
            ),
            "example_out_screenshot": InlineImage(
                graph_report,
                example_out_screenshot.as_posix(),
                width=Mm(50),
            ),
            "task_out_screenshot": InlineImage(
                graph_report,
                task_out_screenshot.as_posix(),
                width=Mm(50),
            ),
            "task_outer": task_outer_file.read_text(),
        }
    )
    graph_report.save(task_report_file)

    return task_py_file.parent


def create_tree_task(task_num: int) -> Path:
    task_type = TaskType.TREE
    normalized_task_num = task_num - 1

    tree_abc_folder = task_type.get_base_path() / "abc"

    # Вычисление кода дерева
    if 0 <= (sub_task_num := normalized_task_num % 50) <= 19:  # Дерево двоичного поиска
        tree_folder = tree_abc_folder / "bst"
        tree_class_name = "BST"

        tree_report = DocxTemplate(tree_folder / "bst_report.docx")

        if sub_task_num % 20 <= 4:  # Указатель (курсор) на родителя
            tree_code = read_abc_file(tree_folder / "parent_pointer_bst.py")
            tree_realization = "Указатель (курсор) на родителя"

        elif sub_task_num % 20 <= 9:  # Список сыновей
            tree_code = read_abc_file(tree_folder / "child_list_bst.py")
            tree_realization = "Список сыновей"

        elif sub_task_num % 20 <= 14:  # Левый сын, правый брат (указатели)
            tree_code = read_abc_file(tree_folder / "left_right_pointer_bst.py")
            tree_realization = "Левый сын, правый брат (указатели)"

        elif sub_task_num % 20 <= 19:  # Левый сын, правый брат (таблица, массив)
            tree_code = read_abc_file(tree_folder / "left_right_table_bst.py")
            tree_realization = "Левый сын, правый брат (таблица, массив)"

    elif 20 <= (sub_task_num := normalized_task_num % 50) <= 34:  # Рандомизированное дерево двоичного поиска
        tree_folder = tree_abc_folder / "randomized_bst"
        tree_class_name = "RandomizedBST"

        tree_report = DocxTemplate(tree_folder / "randomized_bst_report.docx")

        if (sub_task_num - 20) % 15 <= 4:  # Список сыновей
            tree_code = read_abc_file(tree_folder / "child_list_randomized_bst.py")
            tree_realization = "Список сыновей"

        elif (sub_task_num - 20) % 15 <= 9:  # Левый сын, правый брат (указатели)
            tree_code = read_abc_file(tree_folder / "left_right_pointer_randomized_bst.py")
            tree_realization = "Левый сын, правый брат (указатели)"

        elif (sub_task_num - 20) % 15 <= 14:  # Левый сын, правый брат (таблица, массив)
            tree_code = read_abc_file(tree_folder / "left_right_table_randomized_bst.py")
            tree_realization = "Левый сын, правый брат (таблица, массив)"

    elif 35 <= (sub_task_num := normalized_task_num % 50) <= 49:  # AVL-дерево
        tree_class_name = "AVL_BST"
        tree_folder = tree_abc_folder / "avl_bst"

        tree_report = DocxTemplate(tree_folder / "avl_bst_report.docx")

        if (sub_task_num - 35) % 15 <= 4:  # Список сыновей
            tree_code = read_abc_file(tree_folder / "child_list_avl_bst.py")
            tree_realization = "Список сыновей"

        elif (sub_task_num - 35) % 15 <= 9:  # Левый сын, правый брат, указатели
            tree_code = read_abc_file(tree_folder / "left_right_pointer_avl_bst.py")
            tree_realization = "Левый сын, правый брат (указатели)"

        elif (sub_task_num - 35) % 15 <= 14:  # Левый сын, правый брат, массив
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
    tree_operation_line = tree_operation_code.splitlines()[1]
    operation_line_matcher = re.compile(r"\$(?P<OPERATION>.*)\$")
    tree_operation = operation_line_matcher.search(tree_operation_line).group("OPERATION")
    tree_operation_code = tree_operation_code.replace(tree_operation_line, "")

    # Вычисление кода вывода дерева А
    tree_prints_seq = json.loads((tree_abc_folder / "prints.json").read_text())
    if tree_prints_seq[normalized_task_num]:
        tree_a_print_code = r'print("Дерево А в прямом порядке:\n" + str(tree_a.traverse_preorder()))'
        tree_a_print = "Прямой"
    else:
        tree_a_print_code = r'print("Дерево А в обратном порядке:\n" + str(tree_a.traverse_postorder()))'
        tree_a_print = "Обратный"

    # Составление итогового кода
    tree_operation_code = tree_operation_code.replace("# $print_A$", tree_a_print_code).replace(
        "TREE__", tree_class_name
    )

    task_code = tree_code + "\n\n" + tree_operation_code

    # Запись кода в файл
    task_py_file = create_task_file(task_type, task_num)
    task_py_file.write_text(task_code)

    exec_out = get_exec_out(task_py_file)
    task_out_screenshot = create_execution_screenshot(task_py_file.parent, exec_out)

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

    return task_py_file.parent
