import re
from dataclasses import dataclass, field
from pathlib import Path
from pprint import pprint
from subprocess import PIPE, Popen
from textwrap import indent
from typing import Dict, List, Optional, TypeVar

_VT = TypeVar("_VT")


def Some(v: Optional[_VT]) -> _VT:
    assert v is not None
    return v


_SDEF = "$DEF"
_EDEF = "$ENDEF"
_CXDEF = "$CXDEF"

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


@dataclass
class CollectionDef:
    collection_type_name: str
    collection_class_name: str
    collection_code: str
    cxdefs: Dict[str, str] = field(default_factory=dict)


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

        sorts.append(
            SortDef(
                sort_type_name=sort_type_name, sort_func=sort_func, sort_code=sort_code
            )
        )

    return sorts


def prepare_collections(collections_files: List[Path]) -> List[CollectionDef]:

    collections: List[CollectionDef] = []
    cxdef_matcher = re.compile(
        r"(?P<func_def>(def (?P<func_name>.+)\(.+))\$CXDEF: (?P<cxdef>.+)\$"
    )

    for collection_file in collections_files:
        collection_type_name = collection_file.name.split(".")[0]
        collection_file_code = collection_file.read_text()

        lines = []
        start = False
        collection_class = None
        cxdefs: Dict[str, str] = {}
        for line in collection_file_code.splitlines():
            if _SDEF in line:
                start = True

            elif _EDEF in line:
                break

            elif _COLLECTION_CLASS_MARKER in line:
                collection_class = Some(
                    re.search(r"\$Collection: (\w+)\$", line)
                ).group(1)

            if _CXDEF in line:
                func_name = re.sub(cxdef_matcher, r"\g<func_name>", line)
                cxdef = re.sub(cxdef_matcher, r"\g<cxdef>", line)
                line = re.sub(cxdef_matcher, r"\g<func_def>\g<cxdef>", line)

                cxdefs[func_name] = cxdef

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


def main():
    sorts_files = list(SORTS_ABC_DIR.glob("*_sort.py"))
    collections_files = list(COLLECTIONS_ABC_DIR.glob("*.py"))

    sorts = prepare_sorts(sorts_files)
    collections = prepare_collections(collections_files)

    for sort in sorts:
        for collection in collections:
            pprint(collection.cxdefs)

            collection_var = collection.collection_class_name.lower()
            collection_class_name = collection.collection_class_name

            sort_code = sort.sort_code.replace(
                _COLLECTION_CLASS,
                collection_class_name,
            ).replace(
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
            print(
                f"Collection: {collection.collection_type_name}, Sort: {sort.sort_type_name}"
            )

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
