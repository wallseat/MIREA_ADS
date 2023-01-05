import os
import shutil
import sys
import zipfile
from pathlib import Path
from threading import Thread
from typing import List

import yadisk
from pydantic import BaseSettings
from utils.task_utils import (
    TaskType,
    create_graph_task,
    create_linear_task,
    create_tree_task,
)


class Settings(BaseSettings):
    SECRET_TOKEN: str
    FOLDER_PATH: str

    class Config:
        env_file = ".env"


settings = Settings()


def upload_to_yd(disk: yadisk.YaDisk, task_type: TaskType, task_set: List[int]) -> None:
    for task_no in task_set:
        try:
            zip_path = None
            task_folder_path = None
            lab_name = None
            rm = True if task_type != TaskType.GRAPH else False

            path = task_type.get_base_path() / str(task_no)
            if path.exists() and rm:
                shutil.rmtree(path)

            if task_type == TaskType.TREE:
                task_folder_path = create_tree_task(task_no)
            elif task_type == TaskType.LINEAR:
                task_folder_path = create_linear_task(task_no)
            elif task_type == TaskType.GRAPH:
                task_folder_path_exist_before = Path(f"Graph/{task_no}").exists()
                if task_folder_path_exist_before:
                    continue
                try:
                    task_folder_path = create_graph_task(task_no, raise_not_full=True)
                except ValueError as e:
                    print(f"Ошибка при создании задания {task_type}_{task_no}: {e}")
                    if not task_folder_path_exist_before:
                        shutil.rmtree(Path(f"Graph/{task_no}"))

                    continue

            lab_name = task_type.get_task_prefix().capitalize()

            zip_name = f"{lab_name}_{task_no}.zip"
            zip_path = TEMP_PATH / zip_name

            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for entry in task_folder_path.rglob("*"):
                    zip_file.write(entry, entry.relative_to(task_folder_path))

            disk.upload(
                zip_path.as_posix(),
                f"{settings.FOLDER_PATH}/{lab_name}/{zip_path.name}",
                overwrite=True,
                n_retries=5,
                timeout=60,
            )
            added_resources.append(zip_path.name)
        except Exception as e:
            print(f"Ошибка при загрузке задания {lab_name}_{task_no}: {e}")

        else:
            if zip_path:
                zip_path.unlink()
            if task_folder_path:
                shutil.rmtree(task_folder_path)


if __name__ == "__main__":
    disk = yadisk.YaDisk(token=settings.SECRET_TOKEN)

    try:
        disk.mkdir(settings.FOLDER_PATH)
    except yadisk.exceptions.PathExistsError:
        pass
    except yadisk.exceptions.ForbiddenError:
        print("Доступ запрещен, проверьте или обновите ключ")

    TEMP_PATH = Path("temp/")
    if not TEMP_PATH.exists():
        TEMP_PATH.mkdir()
    else:
        for file in TEMP_PATH.iterdir():
            file.unlink()

    WORKERS_NUM = os.cpu_count() // 2
    TOTAL_TASKS = 100

    tasks = []
    labs_set = []
    args = sys.argv[1:]
    if args:
        if "t" in args:
            labs_set.append(TaskType.TREE)
        if "l" in args:
            labs_set.append(TaskType.LINEAR)
        if "g" in args:
            labs_set.append(TaskType.GRAPH)

        if not labs_set:
            labs_set = TaskType

        for arg in args:
            if arg.isdigit():
                task = int(arg)
                if task > 0 and task <= 100:
                    tasks.append(task)
        if not tasks:
            tasks = list(range(1, 100 + 1))

    added_resources = []
    try:
        for lab_type in labs_set:
            lab_name = lab_type.get_task_prefix().capitalize()

            try:
                disk.mkdir(f"{settings.FOLDER_PATH}/{lab_name}")
            except yadisk.exceptions.PathExistsError:
                pass

            tasks_per_worker = len(tasks) // WORKERS_NUM + 1
            _tasks = tasks.copy()

            workers: List[Thread] = []
            while _tasks:
                t = Thread(
                    target=upload_to_yd,
                    args=(disk, lab_type, _tasks[:tasks_per_worker]),
                )
                workers.append(t)
                t.start()
                del _tasks[:tasks_per_worker]

            for worker in workers:
                worker.join()

    except Exception:
        [os.remove(file) for file in TEMP_PATH.iterdir()]
        exit(0)

    print("Добавлены архивы:  " + ", ".join(added_resources))
