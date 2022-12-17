import os
import zipfile
from hashlib import md5
from pathlib import Path
from threading import Thread
from typing import List

import yadisk
from pydantic import BaseSettings
from yadisk.objects.resources import ResourceObject


class Settings(BaseSettings):
    SECRET_TOKEN: str
    FOLDER_PATH: str

    class Config:
        env_file = ".env"


settings = Settings()


def upload_to_yd(disk: yadisk.YaDisk, files: List[Path]) -> None:
    for file in files:
        if file.is_file():
            with open(file, "rb") as f:
                file_hash = md5(f.read()).hexdigest()
            if not disk.exists(f"{settings.FOLDER_PATH}/{lab_type}/{file.name}"):
                disk.upload(
                    file.as_posix(),
                    f"{settings.FOLDER_PATH}/{lab_type}/{file.name}",
                    n_retries=5,
                    timeout=60,
                )
                added_resources.append(file.name)

            else:
                resource: ResourceObject = disk.get_meta(
                    f"{settings.FOLDER_PATH}/{lab_type}/{file.name}"
                )
                if resource["md5"] != file_hash:
                    disk.upload(
                        file.as_posix(),
                        f"{settings.FOLDER_PATH}/{lab_type}/{file.name}",
                        overwrite=True,
                        n_retries=5,
                        timeout=60,
                    )
                    changed_resources.append(file.name)

            os.remove(file)


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

    LAB_TYPES = ["Graph", "Tree", "Linear"]

    WORKERS_NUM = os.cpu_count()

    added_resources = []
    changed_resources = []
    try:
        for lab_type in LAB_TYPES:
            try:
                disk.mkdir(f"{settings.FOLDER_PATH}/{lab_type}")
            except yadisk.exceptions.PathExistsError:
                pass

            root_labs_path = Path(lab_type)
            for task in root_labs_path.iterdir():
                if task.is_dir() and task.name.isdigit():
                    zip_name = f"{lab_type}_{task.name}.zip"

                    with zipfile.ZipFile(
                        TEMP_PATH / zip_name, "w", zipfile.ZIP_DEFLATED
                    ) as zip_file:
                        for entry in task.rglob("*"):
                            zip_file.write(entry, entry.relative_to(task))

            file_per_worker = len(os.listdir(TEMP_PATH)) // WORKERS_NUM + 1
            files = list(TEMP_PATH.iterdir())
            workers: List[Thread] = []
            while files:
                t = Thread(target=upload_to_yd, args=(disk, files[:file_per_worker]))
                workers.append(t)
                t.start()
                del files[:file_per_worker]

            for worker in workers:
                worker.join()

    except Exception:
        [os.remove(file) for file in TEMP_PATH.iterdir()]
        exit(0)

    print("Добавлены архивы:  " + ", ".join(added_resources))
    print("Обновлены архивы:  " + ", ".join(changed_resources))
