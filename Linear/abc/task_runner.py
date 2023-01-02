from ICollection import VT, Collection


def print_collection(collection: Collection[VT]) -> None:
    ...


def some_sort(collection: Collection[VT]) -> Collection[VT]:
    ...


# $DEF
if __name__ == "__main__":
    import sys
    import time
    from random import randint

    if len(sys.argv) < 2 or sys.argv[1] not in ["example", "tests"]:
        print(f"Usage: python3 {sys.argv[0]} [example/tests]")
        exit(1)

    if sys.argv[1] == "example":
        collection = Collection[int]()
        for _ in range(20):
            collection.push(randint(-10000, 10000))

        some_sort(collection)
        print_collection(collection)

    elif sys.argv[1] == "tests":
        tests = 10
        step = None

        for test_num in range(1, tests + 1):
            collection = Collection[int]()

            for _ in range(test_num * step):
                collection.push(randint(-10000, 10000))

            start_time = time.time()
            some_sort(collection)
            total_time = time.time() - start_time

            print(f"Test: {test_num}")
            print(f"Elements count: {test_num * step}")
            print(f"Total time: {total_time}")
            print(f"N_OP: {collection.n_op}")
            print("-------------")
# $ENDEF
