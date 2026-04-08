import io
import os
import socket
import shutil
from pathlib import Path
from typing import Protocol


class StorageAdapter(Protocol):
    def put_bytes(self, path: str, payload: bytes, content_type: str) -> str:
        pass

    def put_file(self, path: str, source_path: str, content_type: str) -> str:
        pass

    def get_to_local_path(self, path: str, target_dir: str) -> str:
        pass

    def delete(self, path: str) -> None:
        pass


class FilesystemStorageAdapter:
    def __init__(self, base_dir: str) -> None:
        self.base_dir = Path(base_dir)

    def put_bytes(self, path: str, payload: bytes, content_type: str) -> str:
        target = self.base_dir / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        return str(target)

    def put_file(self, path: str, source_path: str, content_type: str) -> str:
        target = self.base_dir / path
        target.parent.mkdir(parents=True, exist_ok=True)
        source = Path(source_path)
        if source.resolve() != target.resolve():
            shutil.copyfile(source, target)
        return str(target)

    def get_to_local_path(self, path: str, target_dir: str) -> str:
        candidate = Path(path)
        if candidate.is_absolute() or candidate.exists():
            return str(candidate)
        return str(self.base_dir / candidate)

    def delete(self, path: str) -> None:
        target = self.base_dir / path
        if target.exists():
            target.unlink()


class MinioStorageAdapter:
    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        secure: bool = False,
    ) -> None:
        from minio import Minio

        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )
        self.bucket_name = bucket_name

    def put_bytes(self, path: str, payload: bytes, content_type: str) -> str:
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)
        self.client.put_object(
            self.bucket_name,
            path,
            io.BytesIO(payload),
            len(payload),
            content_type=content_type,
        )
        return f"{self.bucket_name}/{path}"

    def put_file(self, path: str, source_path: str, content_type: str) -> str:
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)
        self.client.fput_object(
            self.bucket_name,
            path,
            source_path,
            content_type=content_type,
        )
        return f"{self.bucket_name}/{path}"

    def get_to_local_path(self, path: str, target_dir: str) -> str:
        target_root = Path(target_dir)
        target_root.mkdir(parents=True, exist_ok=True)
        object_name = self._object_name(path)
        target = target_root / Path(object_name).name
        self.client.fget_object(self.bucket_name, object_name, str(target))
        return str(target)

    def delete(self, path: str) -> None:
        self.client.remove_object(self.bucket_name, self._object_name(path))

    def _object_name(self, path: str) -> str:
        prefix = f"{self.bucket_name}/"
        if path.startswith(prefix):
            return path[len(prefix) :]
        return path


def build_storage_adapter() -> StorageAdapter:
    backend = os.getenv("EMATA_STORAGE_BACKEND", "filesystem").lower()
    if backend == "minio":
        endpoint = os.getenv("EMATA_MINIO_ENDPOINT", "localhost:9000")
        host, _, port = endpoint.partition(":")
        resolved_port = int(port) if port.isdigit() else 9000
        try:
            socket.getaddrinfo(host, resolved_port, socket.AF_UNSPEC, socket.SOCK_STREAM)
        except OSError:
            return FilesystemStorageAdapter(
                base_dir=os.getenv("EMATA_UPLOAD_BASE_DIR", "./tmp/uploads"),
            )
        try:
            adapter = MinioStorageAdapter(
                endpoint=endpoint,
                access_key=os.getenv("EMATA_MINIO_ACCESS_KEY", "minioadmin"),
                secret_key=os.getenv("EMATA_MINIO_SECRET_KEY", "minioadmin"),
                bucket_name=os.getenv("EMATA_MINIO_BUCKET", "knowledge-source-files"),
                secure=os.getenv("EMATA_MINIO_SECURE", "false").lower() == "true",
            )
            adapter.client.bucket_exists(adapter.bucket_name)
            return adapter
        except Exception:
            pass
    return FilesystemStorageAdapter(
        base_dir=os.getenv("EMATA_UPLOAD_BASE_DIR", "./tmp/uploads"),
    )
