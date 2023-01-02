import os
import shutil
import zipfile
from hashlib import md5
from pathlib import Path
from threading import Thread
from typing import List

import yadisk
from pydantic import BaseSettings
from utils.task_utils import TaskType, create_linear_task, create_tree_task
from yadisk.objects.resources import ResourceObject


class Settings(BaseSettings):
    SECRET_TOKEN: str
    FOLDER_PATH: str

    class Config:
        env_file = ".env"


settings = Settings()


def upload_to_yd_old(disk: yadisk.YaDisk, files: List[Path]) -> None:
    for file in files:
        if file.is_file():
            with open(file, "rb") as f:
                file_hash = md5(f.read()).hexdigest()
            if not disk.exists(f"{settings.FOLDER_PATH}/{lab_name}/{file.name}"):
                disk.upload(
                    file.as_posix(),
                    f"{settings.FOLDER_PATH}/{lab_name}/{file.name}",
                    n_retries=5,
                    timeout=60,
                )
                added_resources.append(file.name)

            else:
                resource: ResourceObject = disk.get_meta(f"{settings.FOLDER_PATH}/{lab_name}/{file.name}")
                if resource["md5"] != file_hash:
                    disk.upload(
                        file.as_posix(),
                        f"{settings.FOLDER_PATH}/{lab_name}/{file.name}",
                        overwrite=True,
                        n_retries=5,
                        timeout=60,
                    )
                    changed_resources.append(file.name)

            os.remove(file)


def upload_to_yd(disk: yadisk.YaDisk, task_type: TaskType, task_no_s: int, task_no_e: int) -> None:
    for task_no in range(task_no_s, task_no_e + 1):
        try:
            zip_path = None
            task_folder_path = None
            lab_name = None

            path = task_type.get_base_path() / str(task_no)
            if path.exists():
                shutil.rmtree(path)

            if task_type == TaskType.TREE:
                task_folder_path = create_tree_task(task_no)
            elif task_type == TaskType.LINEAR:
                task_folder_path = create_linear_task(task_no)
            else:
                raise NotImplementedError

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
            changed_resources.append(zip_path.name)
        except Exception as e:
            if lab_name:
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

    added_resources = []
    changed_resources = []
    try:
        for lab_type in TaskType:
            lab_name = lab_type.get_task_prefix().capitalize()

            try:
                disk.mkdir(f"{settings.FOLDER_PATH}/{lab_name}")
            except yadisk.exceptions.PathExistsError:
                pass

            if lab_type in (TaskType.TREE, TaskType.LINEAR):
                tasks_per_worker = 100 // WORKERS_NUM + 1
                from_task = 1

                workers: List[Thread] = []
                while from_task < 100:
                    t = Thread(
                        target=upload_to_yd,
                        args=(disk, lab_type, from_task, min(100, from_task + tasks_per_worker)),
                    )
                    workers.append(t)
                    t.start()
                    from_task += tasks_per_worker + 1

                for worker in workers:
                    worker.join()

            else:
                # for task in lab_type.get_base_path().iterdir():
                #     if task.is_dir() and task.name.isdigit():
                #         zip_name = f"{lab_name}_{task.name}.zip"

                #         with zipfile.ZipFile(TEMP_PATH / zip_name, "w", zipfile.ZIP_DEFLATED) as zip_file:
                #             for entry in task.rglob("*"):
                #                 zip_file.write(entry, entry.relative_to(task))

                # file_per_worker = len(os.listdir(TEMP_PATH)) // WORKERS_NUM + 1
                # files = list(TEMP_PATH.iterdir())
                # workers: List[Thread] = []
                # while files:
                #     t = Thread(target=upload_to_yd_old, args=(disk, files[:file_per_worker]))
                #     workers.append(t)
                #     t.start()
                #     del files[:file_per_worker]

                # for worker in workers:
                #     worker.join()
                pass

    except Exception:
        [os.remove(file) for file in TEMP_PATH.iterdir()]
        exit(0)

    print("Добавлены архивы:  " + ", ".join(added_resources))
    print("Обновлены архивы:  " + ", ".join(changed_resources))
