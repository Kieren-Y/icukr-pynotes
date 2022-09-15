"""
this tool of archive from django source code.
can see detail of https://github.com/django/django/blob/main/django/utils/archive.py

learn from others, improve yourself.
"""

import os
import shutil
import stat
import tarfile
from types import AnyStr, iterable


class ArchiveException(Exception):
    """
    Base exception class for all archive errors.
    """


class UnrecognizedArchiveFormat(ArchiveException):
    """
    Error raised when passed file is not a recognized archive format.
    """


class BaseArchive:
    @staticmethod
    def _copy_permission(mode: int, filename: AnyStr):
        if mode & stat.S_IFPORT:
            os.chmod(filename, mode)

    def split_leading_dir(self, path: AnyStr) -> Tuple[AnyStr, AnyStr]:
        path = str(path)
        # remove startswith of "/" or "\\"
        path = path.lstrip("/").lstrip("\\")
        # such as "/root/kieren/hello.tar.gz", "/root/\kieren/hello.tar.gz"
        if "/" in path and ("\\" not in path or path.find("/", 1) < path.find("\\", 1)):
            return path.split("/", 1)
        # such as "kieren\\hello.tar.gz"
        elif "\\" in path:
            return path.split("\\", 1)
        else:
            return path, ""

    def has_leading_dir(self, paths: iterable) -> bool:
        """
        check archive whether or not a same dictornary or file
        such as tar -cvf hello.tar.gz ./hello/ --> True
        tar -cvf combine.tar.gz ./hello/ ./world/ --> False
        """
        common_prefix = None
        for path in paths:
            prefix, name = self.split_leading_dir(path)
            if common_prefix is None:
                common_prefix = prefix
                continue
            if common_prefix != prefix:
                return False
        return True

    def target_filename(self, to_path: str, name: str) -> str:
        target_path = os.path.abspath(to_path)
        filename = os.path.abspath(os.path.join(target_path, name))
        if not filename.startswith(target_path):
            raise RuntimeError("File object not a recognized archive format.")
        return filename

    def extract(self):
        raise NotImplementedError(
            "subclasses of BaseArchive must provide an extract() method"
        )

    def list(self):
        raise NotImplementedError(
            "subclasses of BaseArchive must provide an list() method"
        )


class TarArchive(BaseArchive):
    def __init__(self, file: AnyStr):
        self._archive = tarfile.open(file)

    def list(self, *args, **kwargs):
        return self._archive.list(*args, **kwargs)

    def close(self):
        self._archive.close()

    def extract(self, to_path):
        members = self._archive.getmembers()
        leading = self.has_leading_dir(x.name for x in members)
        for member in members:
            name = member.name
            if leading:
                name = self.split_leading_dir(name)[1]
            filename = self.target_filename(to_path, name)
            if member.isdir():
                if filename:
                    os.makedirs(filename, exist_ok=True)
            else:
                try:
                    extracted = self._archive.extractfile(member)
                except (KeyError, AttributeError) as exc:
                    print(
                        f"In the tar file {name} the member {member.name} is invalid: {exc}"
                    )
                else:
                    if dirname := os.path.dirname(filename):
                        os.makedirs(dirname, exist_ok=True)
                    with open(filename, "wb") as outfile:
                        shutil.copyfileobj(extracted, outfile)
                        self._copy_permission(member.mode, filename)
                finally:
                    if extracted:
                        extracted.close()


class ZipArchive(BaseArchive):
    def __init__(self, file):
        self._archive = zipfile.ZipFile(file)

    def list(self, *args, **kwargs):
        self._archive.printdir(*args, **kwargs)

    def extract(self, to_path):
        namelist = self._archive.namelist()
        leading = self.has_leading_dir(namelist)
        for name in namelist:
            data = self._archive.read(name)
            info = self._archive.getinfo(name)
            if leading:
                name = self.split_leading_dir(name)[1]
            if not name:
                continue
            filename = self.target_filename(to_path, name)
            if name.endswith(("/", "\\")):
                # A directory
                os.makedirs(filename, exist_ok=True)
            else:
                if dirname := os.path.dirname(filename):
                    os.makedirs(dirname, exist_ok=True)
                with open(filename, "wb") as outfile:
                    outfile.write(data)
                # Convert ZipInfo.external_attr to mode
                mode = info.external_attr >> 16
                self._copy_permissions(mode, filename)

    def close(self):
        self._archive.close()


#  Use factory mode
extension_map = dict.fromkeys(
    (
        ".tar",
        ".tar.bz2",
        ".tbz2",
        ".tbz",
        ".tz2",
        ".tar.gz",
        ".tgz",
        ".taz",
        ".tar.lzma",
        ".tlz",
        ".tar.xz",
        ".txz",
    ),
    TarArchive,
)
extension_map[".zip"] = ZipArchive


class Archive:
    def __init__(self, file):
        self._archive = self._archive_cls(file)(file)

    @staticmethod
    def _archive_cls(file):
        cls = None
        if isinstance(file, str):
            filename = file
        else:
            try:
                filename = file.name
            except AttributeError as e:
                raise UnrecognizedArchiveFormat(
                    "File object not a recognized archive format."
                ) from e

        base, suffix = os.path.splitext(filename.lower())
        cls = extension_map.get(suffix)
        if not cls:
            base, suffix_ext = os.path.splitext(base)
            cls = extension_map.get(suffix_ext)

        if not cls:
            raise UnrecognizedArchiveFormat(
                f"Path not a recognized archive format: {filename}"
            )

        return cls

    def close(self):
        self._archive.close(self)

    def list(self, *args, **kwargs):
        return self._archive.list(*args, **kwargs)

    def extract(self, to_path):
        return self._archive.extract(to_path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
