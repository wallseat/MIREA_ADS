import re
import sympy
from dataclasses import dataclass, field
from pathlib import Path
from pprint import pprint
from subprocess import PIPE, Popen
from textwrap import indent
from typing import Dict, List, Optional, TypeVar, Tuple
from sympy.parsing.sympy_parser import parse_expr
from sympy.core import Expr, Number

_VT = TypeVar("_VT")


def Some(v: Optional[_VT]) -> _VT:
    assert v is not None
    return v


_SDEF = "$DEF"
_EDEF = "$ENDEF"
_CXDEF = "$CXDEF"
_CXPUSH = "$CX_PUSH"
_CXPOP = "$CX_POP"
_CXPOPBACK = "$CX_POP_BACK"
_CXEXPR = "$CX_EXPR"

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
            if _SDEF in line:
                s_line = i + 1
            if _EDEF in line:
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
    cxdef_matcher = re.compile(r"(?P<func_def>(def (?P<func_name>.+)\(.+))\$CXDEF: (?P<cxdef>.+)\$")

    for collection_file in collections_files:
        collection_type_name = collection_file.name.split(".")[0]
        collection_file_code = collection_file.read_text()

        lines = []
        start = False
        collection_class = None
        class_section = False
        cxdefs: _T_CXDEFS = {}
        for line in collection_file_code.splitlines():
            if _SDEF in line:
                start = True

            elif _EDEF in line:
                break

            elif _COLLECTION_CLASS_MARKER in line:
                collection_class = Some(re.search(r"\$Collection: (\w+)\$", line)).group(1)

            elif "class" in line and collection_class and collection_class in line:
                class_section = True

            elif class_section and line and not line.startswith(("    ", "\t")):
                class_section = False

            elif _CXDEF in line:
                func_name = re.sub(cxdef_matcher, r"\g<func_name>", line).strip()
                cxdef = re.sub(cxdef_matcher, r"\g<cxdef>", line).strip()
                line = re.sub(cxdef_matcher, r"\g<func_def>\g<cxdef>", line)

                if class_section:
                    func_name = f"{_COLLECTION_CLASS}__{func_name}"

                cxdefs[func_name] = parse_expr(cxdef)

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
    cxexpr_matcher = re.compile(r"(?P<LINE>.+)(?P<CX_EXPR>(\$CX_EXPR: (?P<EXPR>(.+))\$))")

    expr_stack: List[str] = []
    stack_frames: List[Tuple[int, int]] = []  # (line_no, stack_frame)
    lines: List[str] = []

    for i, line in enumerate(code.splitlines()):
        if _CXEXPR in line:
            str_expr = re.sub(cxexpr_matcher, r"\g<EXPR>", line).strip()

            if not str_expr.endswith(("*", "/", "+", "-", "(", ")", "**")):
                str_expr = str(parse_expr(str_expr, local_dict=cxdefs))

            expr_stack.append(str_expr)

            line = re.sub(cxexpr_matcher, r"\g<LINE>" + str_expr, line)

        if _CXPUSH in line:
            stack_frames.append(
                (i, len(expr_stack)),
            )

        elif _CXPOP in line:
            line_no, stack_frame = stack_frames.pop()
            str_expr = " ".join(str_expr_stack[stack_frame:])

            print(str_expr)

            expr = parse_expr(str_expr, local_dict=cxdefs)

            if _CXPOPBACK in line:
                line = line.replace(_CXPOPBACK, "")
                lines[line_no] = lines[line_no].replace(_CXPUSH, str(expr))
            else:
                line = line.replace(_CXPOP, str(expr))
                lines[line_no] = lines[line_no].replace(_CXPUSH, "")

        lines.append(line)

        print("\n".join(lines) + "\n\n")


def main():
    sorts_files = list(SORTS_ABC_DIR.glob("count_sort.py"))
    collections_files = list(COLLECTIONS_ABC_DIR.glob("stack_array.py"))

    sorts = prepare_sorts(sorts_files)
    collections = prepare_collections(collections_files)

    for sort in sorts:
        for collection in collections:
            collection_var = collection.collection_class_name.lower()
            collection_class_name = collection.collection_class_name

            solve_cxdefs(sort.sort_code, collection.cxdefs)

            sort_code = sort.sort_code.replace(_COLLECTION_CLASS, collection_class_name,).replace(
                _COLLECTION_VAR,
                collection_var,
            )

            code = collection.collection_code + sort_code
            code += (
                "\nif __name__ == '__main__':\n"
                "\tfrom random import randint\n"
                "\tdata = [randint(-99, 99) for _ in range(200)]\n"
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

            tmp_py.unlink()


if __name__ == "__main__":
    main()
