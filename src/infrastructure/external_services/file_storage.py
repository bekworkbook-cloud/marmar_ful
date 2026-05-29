import os
import shutil
from fastapi import UploadFile

class IFileStorage:
    async def save(self, file: UploadFile, directory: str) -> str:
        raise NotImplementedError

class LocalFileStorage(IFileStorage):
    async def save(self, file: UploadFile, directory: str) -> str:
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_path