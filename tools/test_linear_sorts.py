import re
from dataclasses import dataclass
from pathlib import Path
from subprocess import PIPE, Popen
from textwrap import indent
from typing import List

_SDEF = "$DEF$"
_EDEF = "$ENDEF$"
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
        sort_func = re.search(r"def (\w+_sort)\(", sort_code).group(1)

        sorts.append(
            SortDef(
                sort_type_name=sort_type_name, sort_func=sort_func, sort_code=sort_code
            )
        )

    return sorts


def prepare_collections(collections_files: List[Path]) -> List[CollectionDef]:

    collections: List[CollectionDef] = []

    for collection_file in collections_files:
        collection_type_name = collection_file.name.split(".")[0]
        collection_file_code = collection_file.read_text().splitlines()

        s_line = None
        e_line = None
        collection_class = None
        for i, line in enumerate(collection_file_code):
            if _SDEF in line:
                s_line = i + 1
            if _EDEF in line:
                e_line = i
                break
            if _COLLECTION_CLASS_MARKER in line:
                collection_class = re.search(r"\$Collection: (\w+)\$", line).group(1)

        if s_line is None or e_line is None or collection_class is None:
            raise ValueError(f"Invalid collection definition in {collection_file}")

        collection_code = "\n".join(collection_file_code[s_line:e_line])

        collections.append(
            CollectionDef(
                collection_type_name=collection_type_name,
                collection_class_name=collection_class,
                collection_code=collection_code,
            )
        )

    return collections


def main():
    sorts_files = list(SORTS_ABC_DIR.glob("*_sort.py"))
    collections_files = list(COLLECTIONS_ABC_DIR.glob("stack_*.py"))

    sorts = prepare_sorts(sorts_files)
    collections = prepare_collections(collections_files)

    for sort in sorts:
        for collection in collections:
            collection_var = collection.collection_class_name.lower()
            collection_class_name = collection.collection_class_name

            sort_code = sort.sort_code.replace(
                _COLLECTION_CLASS, collection_class_name
            ).replace(_COLLECTION_VAR, collection_var)

            code = collection.collection_code + sort_code
            code += (
                "\nif __name__ == '__main__':\n"
                "\tfrom random import randint\n"
                "\tdata = [randint(-99, 99) for _ in range(25)]\n"
                f"\t{collection_var} = {collection_class_name}[int]()\n"
                "\tfor el in data:\n"
                f"\t\t{collection_var}.push(el)\n"
                "\tdata.sort()\n"
                f"\t{sort.sort_func}({collection_var})\n"
                "\tfor i, el in enumerate(data):\n"
                f"\t\tassert el == seek({collection_var}, i), f'index: {{i}}, expected {{el}}, got {{seek({collection_var}, i)}}'\n"
            )
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
