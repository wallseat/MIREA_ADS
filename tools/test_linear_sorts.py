from pathlib import Path
from subprocess import PIPE, Popen
from textwrap import indent

from utils.linear_utils import (
    COLLECTIONS_ABC_DIR,
    SORTS_ABC_DIR,
    merge_collection_sort_code,
    prepare_collection,
    prepare_sort,
)


def main():
    sorts_files = list(SORTS_ABC_DIR.glob("*_sort.py"))
    collections_files = list(COLLECTIONS_ABC_DIR.glob("*.py"))

    for sort_file in sorts_files:
        sort = prepare_sort(sort_file)

        for collection_file in collections_files:
            collection = prepare_collection(collection_file)

            code = merge_collection_sort_code(collection, sort)

            print(f"Collection: {collection.collection_type_name}, Sort: {sort.sort_type_name}")
            print("F(n):", sort.sort_asymptotic)
            print("O(F(n)):", sort.sort_bigO_asymptotic)

            code += (
                "\nif __name__ == '__main__':\n"
                "\tfrom random import randint\n"
                "\tdata = [randint(-99, 99) for _ in range(20)]\n"
                f"\t{collection.collection_var_name} = {collection.collection_class_name}[int]()\n"
                "\tfor el in data:\n"
                f"\t\t{collection.collection_var_name}.push(el)\n"
                "\tdata.sort()\n"
                f"\t{sort.sort_func}({collection.collection_var_name})\n"
                "\tprint('Expected:')\n"
                "\tprint(data)\n"
                "\tprint('Got:')\n"
                f"\tprint_{collection.collection_var_name}({collection.collection_var_name})\n"
                "\tfor i, el in enumerate(data):\n"
                f"\t\tassert el == seek({collection.collection_var_name}, i), f'index: {{i}}, expected {{el}}, got {{seek({collection.collection_var_name}, i)}}'\n"
            ).replace("\t", "    ")

            tmp_py = Path("tmp.py")
            tmp_py.write_text(code)

            p = Popen(
                ["python", tmp_py],
                stdout=PIPE,
                stderr=PIPE,
                text=True,
            )
            out, err = p.communicate()
            if p.returncode:
                print("Error occurred:")
                print(indent(str(err), "\t"))
                print("Sort output:")
                print(indent(str(out), "\t"))

            tmp_py.unlink()
            print("---------------------------------")


if __name__ == "__main__":
    main()
