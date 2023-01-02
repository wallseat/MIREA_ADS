import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple, TypeVar

import sympy
from sympy.core import Expr, Number
from sympy.parsing.sympy_parser import parse_expr

_VT = TypeVar("_VT")


def Some(v: Optional[_VT]) -> _VT:
    assert v is not None
    return v


_DEF = "$DEF"
_ENDEF = "$ENDEF"
_CX_DEF = "$CX_DEF"
_CX_PUSH = "$CX_PUSH"
_CX_POP = "$CX_POP"
_CX_POP_BACK = "$CX_POP_BACK"
_CX_EXPR = "$CX_EXPR"

_COLLECTION_CLASS = "Collection"
_COLLECTION_VAR = "collection"
_COLLECTION_CLASS_MARKER = "$Collection"


LINEAR_ABC_DIR = Path("Linear/abc")

SORTS_ABC_DIR = LINEAR_ABC_DIR / "sorts"
COLLECTIONS_ABC_DIR = LINEAR_ABC_DIR / "collections"


_T_CXDEFS = Dict[str, Expr | Number]


@dataclass
class SortDef:
    sort_type_name: str
    sort_func: str
    sort_code: str
    sort_asymptotic: Optional[Expr] = None
    sort_bigO_asymptotic: Optional[Expr] = None
    cxdefs: _T_CXDEFS = field(default_factory=dict)


@dataclass
class CollectionDef:
    collection_type_name: str
    collection_class_name: str
    collection_var_name: str
    collection_code: str
    cxdefs: _T_CXDEFS = field(default_factory=dict)


def prepare_sort(sort_file: Path) -> SortDef:
    sort_type_name = sort_file.name.split(".")[0]
    sort_file_code = sort_file.read_text().splitlines()

    s_line = None
    e_line = None
    for i, line in enumerate(sort_file_code):
        if _DEF in line:
            s_line = i + 1
        if _ENDEF in line:
            e_line = i
            break

    if s_line is None or e_line is None:
        raise ValueError(f"Invalid sort definition in {sort_file}")

    sort_code = "\n".join(sort_file_code[s_line:e_line])
    sort_func = Some(
        re.search(r"def (\w+_sort)\(", sort_code),
    ).group(1)

    return SortDef(sort_type_name=sort_type_name, sort_func=sort_func, sort_code=sort_code)


def prepare_collection(collection_file: Path) -> CollectionDef:
    cxdef_matcher = re.compile(
        r"(?P<FUNC_DEF>(def (?P<FUNC_NAME>.+)\(.+))" + re.escape(_CX_DEF) + r": (?P<CX_DEF>.+)\$"
    )

    collection_type_name = collection_file.name.split(".")[0]
    collection_file_code = collection_file.read_text()

    lines = []
    start = False
    collection_class = None
    class_section = False
    cxdefs: _T_CXDEFS = {}
    for line in collection_file_code.splitlines():
        if _DEF in line:
            start = True
            continue

        elif _ENDEF in line:
            break

        elif _COLLECTION_CLASS_MARKER in line:
            collection_class = Some(
                re.search(
                    re.escape(_COLLECTION_CLASS_MARKER) + r": (\w+)\$",
                    line,
                )
            ).group(1)
            collection_var = collection_class.lower()

        elif "class" in line and collection_class and collection_class in line:
            class_section = True

        elif class_section and line and not line.startswith(("    ", "\t")):
            class_section = False

        elif _CX_DEF in line:
            func_name = re.sub(cxdef_matcher, r"\g<FUNC_NAME>", line).strip()
            cxdef = re.sub(cxdef_matcher, r"\g<CX_DEF>", line).strip()
            line = re.sub(cxdef_matcher, r"\g<FUNC_DEF>\g<CX_DEF>", line)

            if class_section:
                func_name = f"{_COLLECTION_CLASS}__{func_name}"

            try:
                cxdefs[func_name] = parse_expr(cxdef)
            except Exception as e:
                raise ValueError(f"Invalid cxdef in {collection_file}. Line\n{line}") from e

        if start:
            lines.append(line)

    if not start or not collection_class:
        raise ValueError(f"Invalid collection definition in {collection_file}")

    collection_code = "\n".join(lines)

    return CollectionDef(
        collection_type_name=collection_type_name,
        collection_class_name=collection_class,
        collection_var_name=collection_var,
        collection_code=collection_code,
        cxdefs=cxdefs,
    )


def solve_cxdefs(sort: SortDef, collection: CollectionDef) -> str:
    cxexpr_matcher = re.compile(r"(?P<LINE>.+)(" + re.escape(_CX_EXPR) + r": (?P<EXPR>(.+))\$)")
    cxpush_matcher = re.compile(r"(?P<LINE>.+)(" + re.escape(_CX_PUSH) + r": (?P<EXPR>(.+))\$)")
    cxdef_cxpush_matcher = re.compile(
        r"(?P<FUNC_DEF>(def (?P<FUNC_NAME>.+)\(.+))"
        + re.escape(_CX_DEF)
        + " "
        + re.escape(_CX_PUSH)
        + r": (?P<EXPR>.+)\$"
    )

    cur_expr: Expr = 0
    expr_stack: List[Expr] = []
    push_stack: List[Tuple[int, Expr]] = []  # push line_no, push expr
    lines: List[str] = []

    sort_code = sort.sort_code
    for i, line in enumerate(sort_code.splitlines()):
        if _CX_EXPR in line:
            str_expr = re.sub(cxexpr_matcher, r"\g<EXPR>", line)

            expr = parse_expr(str_expr, local_dict=collection.cxdefs | sort.cxdefs)
            if not cur_expr:
                cur_expr = expr
            else:
                cur_expr += expr

            str_expr = str(expr)

            line = re.sub(cxexpr_matcher, r"\g<LINE>" + str_expr, line)

        if _CX_PUSH in line:
            cx_def_name = None
            if _CX_DEF in line:
                str_expr = re.sub(cxdef_cxpush_matcher, r"\g<EXPR>", line).strip()
                cx_def_name = re.sub(cxdef_cxpush_matcher, r"\g<FUNC_NAME>", line).strip()
                line = line.replace(_CX_DEF, "")
            else:
                str_expr = re.sub(cxpush_matcher, r"\g<EXPR>", line).strip()

            expr = parse_expr(str_expr, local_dict=collection.cxdefs | sort.cxdefs)

            push_stack.append((i, expr, cx_def_name))

            expr_stack.append(cur_expr)
            cur_expr = 0

        elif _CX_POP in line:
            line_no, expr, cx_def_name = push_stack.pop()
            cur_expr *= expr
            if cx_def_name is not None:
                sort.cxdefs[cx_def_name] = cur_expr

            if _CX_POP_BACK in line:
                line = line.replace(_CX_POP_BACK, "")
                lines[line_no] = re.sub(
                    cxpush_matcher,
                    r"\g<LINE>"
                    + str(
                        cur_expr.simplify(valuate=True).expand(),
                    ),
                    lines[line_no],
                )
            else:
                line = line.replace(
                    _CX_POP,
                    str(
                        cur_expr.simplify(evaluate=True).expand(),
                    ),
                )
                lines[line_no] = re.sub(
                    cxpush_matcher,
                    r"\g<LINE>" + str(expr) + " * (",
                    lines[line_no],
                )

            if line.strip() == "#":
                line = ""

            cur_expr += expr_stack.pop()

        lines.append(line)

    sort_asymptotic = cur_expr.simplify(evaluate=True).expand()
    sort.sort_asymptotic = sort_asymptotic

    max_powered_part = str(sort_asymptotic).split(" ", maxsplit=1)[0]
    if max_powered_part[0].isdigit():
        max_powered_part = max_powered_part.split("*", maxsplit=1)[1]  # remove number multiplier ex: 2*n -> n
    sort_bigO_asymptotic = parse_expr(max_powered_part)

    sort.sort_bigO_asymptotic = sort_bigO_asymptotic

    return "\n".join(lines)


def merge_collection_sort_code(collection: CollectionDef, sort: SortDef) -> str:
    sort_code = solve_cxdefs(sort, collection)
    sort_code = sort_code.replace(_COLLECTION_CLASS, collection.collection_class_name,).replace(
        _COLLECTION_VAR,
        collection.collection_var_name,
    )

    code = collection.collection_code + sort_code

    return code


def prepare_task_runner_code(
    collection: CollectionDef, sort: SortDef, task_runner_file: Path, step: int = 100
) -> str:
    task_runner_code = task_runner_file.read_text().splitlines()

    s_line = None
    e_line = None
    for i, line in enumerate(task_runner_code):
        if _DEF in line:
            s_line = i + 1
        if _ENDEF in line:
            e_line = i
            break

    if s_line is None or e_line is None:
        raise ValueError(f"Invalid runner definition in {task_runner_file}")

    task_runner_code = "\n".join(task_runner_code[s_line:e_line])

    task_runner_code = (
        task_runner_code.replace(
            _COLLECTION_CLASS,
            collection.collection_class_name,
        )
        .replace(
            _COLLECTION_VAR,
            collection.collection_var_name,
        )
        .replace(
            "some_sort",
            sort.sort_func,
        )
        .replace("step = None", f"step = {step}")
    )

    return task_runner_code


def get_n_op(sort: SortDef, n: int) -> Tuple[float, float]:
    subs = {"n": n, "log": lambda x: sympy.log(x, 2)}

    return (
        int(sort.sort_asymptotic.subs(subs).evalf()),
        int(sort.sort_bigO_asymptotic.subs(subs).evalf()),
    )
