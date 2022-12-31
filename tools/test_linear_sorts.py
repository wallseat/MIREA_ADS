import re
from dataclasses import dataclass, field
from pathlib import Path
from subprocess import PIPE, Popen
from textwrap import indent
from typing import Dict, List, Optional, Tuple, TypeVar

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


@dataclass
class SortDef:
    sort_type_name: str
    sort_func: str
    sort_code: str


_T_CXDEFS = Dict[str, Expr | Number]


@dataclass
class CollectionDef:
    collection_type_name: str
    collection_class_name: str
    collection_code: str
    cxdefs: _T_CXDEFS = field(default_factory=dict)


def prepare_sorts(sorts_files: List[Path]) -> List[SortDef]:
    sorts: List[SortDef] = []

    for sort_file in sorts_files:
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

        sorts.append(SortDef(sort_type_name=sort_type_name, sort_func=sort_func, sort_code=sort_code))

    return sorts


def prepare_collections(collections_files: List[Path]) -> List[CollectionDef]:
    collections: List[CollectionDef] = []
    cxdef_matcher = re.compile(
        r"(?P<FUNC_DEF>(def (?P<FUNC_NAME>.+)\(.+))" + re.escape(_CX_DEF) + r": (?P<CX_DEF>.+)\$"
    )

    for collection_file in collections_files:
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

        collections.append(
            CollectionDef(
                collection_type_name=collection_type_name,
                collection_class_name=collection_class,
                collection_code=collection_code,
                cxdefs=cxdefs,
            )
        )

    return collections


def solve_cxdefs(code: str, cxdefs: _T_CXDEFS) -> str:
    cxexpr_matcher = re.compile(r"(?P<LINE>.+)(" + re.escape(_CX_EXPR) + r": (?P<EXPR>(.+))\$)")
    cxpush_matcher = re.compile(r"(?P<LINE>.+)(" + re.escape(_CX_PUSH) + r": (?P<EXPR>(.+))\$)")

    cur_expr: Expr = 0
    expr_stack: List[Expr] = []
    push_stack: List[Tuple[int, Expr]] = []  # push line_no, push expr
    lines: List[str] = []

    for i, line in enumerate(code.splitlines()):
        if _CX_EXPR in line:
            str_expr = re.sub(cxexpr_matcher, r"\g<EXPR>", line)

            expr = parse_expr(str_expr, local_dict=cxdefs)
            if not cur_expr:
                cur_expr = expr
            else:
                cur_expr += expr

            str_expr = str(expr)

            line = re.sub(cxexpr_matcher, r"\g<LINE>" + str_expr, line)

        if _CX_PUSH in line:
            str_expr = re.sub(cxpush_matcher, r"\g<EXPR>", line).strip()

            expr = parse_expr(str_expr, local_dict=cxdefs)

            push_stack.append((i, expr))

            expr_stack.append(cur_expr)
            cur_expr = 0

        elif _CX_POP in line:
            line_no, expr = push_stack.pop()
            cur_expr *= expr

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

    return "\n".join(lines)


def main():
    sorts_files = list(SORTS_ABC_DIR.glob("selection_sort.py"))
    collections_files = list(COLLECTIONS_ABC_DIR.glob("queue_array.py"))

    sorts = prepare_sorts(sorts_files)
    collections = prepare_collections(collections_files)

    for sort in sorts:
        for collection in collections:
            collection_var = collection.collection_class_name.lower()
            collection_class_name = collection.collection_class_name

            sort_code = solve_cxdefs(sort.sort_code, collection.cxdefs)

            sort_code = sort_code.replace(_COLLECTION_CLASS, collection_class_name,).replace(
                _COLLECTION_VAR,
                collection_var,
            )

            code = collection.collection_code + sort_code
            code += (
                "\nif __name__ == '__main__':\n"
                "\tfrom random import randint\n"
                "\tdata = [randint(-99, 99) for _ in range(100)]\n"
                f"\t{collection_var} = {collection_class_name}[int]()\n"
                "\tfor el in data:\n"
                f"\t\t{collection_var}.push(el)\n"
                "\tdata.sort()\n"
                f"\t{sort.sort_func}({collection_var})\n"
                "\tfor i, el in enumerate(data):\n"
                f"\t\tassert el == seek({collection_var}, i), f'index: {{i}}, expected {{el}}, got {{seek({collection_var}, i)}}'\n"
            ).replace("\t", "    ")
            print(f"Collection: {collection.collection_type_name}, Sort: {sort.sort_type_name}")

            tmp_py = Path("tmp.py")
            tmp_py.write_text(code)

            p = Popen(
                ["python", tmp_py],
                stdout=PIPE,
                stderr=PIPE,
                text=True,
            )
            _, err = p.communicate()
            if p.returncode:
                print("Error occurred:")
                print(indent(str(err), "\t"))

            # tmp_py.unlink()


if __name__ == "__main__":
    main()
