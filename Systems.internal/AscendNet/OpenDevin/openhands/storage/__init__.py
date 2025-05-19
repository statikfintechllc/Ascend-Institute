from openhands.storage.files import FileStore
from openhands.storage.local import LocalFileStore
from openhands.storage.memory import InMemoryFileStore
from openhands.storage.s3 import S3FileStore

# REMOVE or COMMENT THIS LINE — it's your villain
# from openhands.storage.google_cloud import GoogleCloudFileStore


def get_file_store(file_store: str, file_store_path: str | None = None) -> FileStore:
    if file_store == "local":
        if file_store_path is None:
            raise ValueError("file_store_path is required for local file store")
        return LocalFileStore(file_store_path)
    elif file_store == "s3":
        return S3FileStore(file_store_path)
    elif file_store == "google_cloud":
        raise NotImplementedError("Google Cloud storage is disabled.")
    return InMemoryFileStore()
