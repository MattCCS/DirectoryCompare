"""
Compares two directories and assigns scores based on their similarities.
"""

import pathlib
import uuid
from typing import Dict, Generator

import xxhash


def fast_read(path, buffer=1024 * 1024):
    """
    Yield the contents of the given filepath in chunks at most `buffer` long.
    """
    with open(path, "rb") as infile:
        while data := infile.read(buffer):
            yield data


def fast_hash(path):
    """
    Hashes the contents of the given filepath in chunks.
    Returns an int digest of the XXH3_128 hash.
    """
    hash_obj = xxhash.xxh3_128()

    for data in fast_read(path):
        hash_obj.update(data)

    return hash_obj.intdigest()


class File:
    HASHES = {}

    def __init__(self, filepath: str):
        self._filepath = pathlib.Path(filepath)
        self._name = self._filepath.name
        self._hash: int = None  # calculated lazily

    def hash(self):
        if self._hash:
            pass
        elif self._filepath in File.HASHES:
            self._hash = File.HASHES[self._filepath]
        else:
            self._hash = fast_hash(self._filepath)
            File.HASHES[self._filepath] = self._hash
        return self._hash


class Directory:
    # objects = {}

    def __init__(self, filepath: str):
        # Directory.objects[uuid.uuid4()] = self
        self._filepath: str = pathlib.Path(filepath)
        self._files: Dict[str, str] = {}
        self._directories: Dict[str, Directory] = {}
        self._hash: int = None  # calculated lazily
        self._depth: int = None  # calculated lazily
        self.load_contents()

    def load_contents(self):
        for e in self._filepath.glob("*"):
            path = e.absolute()
            if e.is_file():
                self._files[path] = File(path)
            elif e.is_dir():
                self._directories[path] = Directory(path)

    def files(self) -> Generator[File, None, None]:
        yield from self._files.values()
        for d in self._directories.values():
            yield from d.files()

    def directories(self) -> Generator[str, None, None]:
        yield from self._directories.values()
        for d in self._directories.values():
            yield from d.directories()

    def directory_paths(self, relative_to=None) -> Generator[str, None, None]:
        if relative_to:
            yield str(self._filepath.relative_to(relative_to))
        else:
            yield str(self._filepath)

        for d in self._directories.values():
            yield from d.directory_paths(relative_to=relative_to or self._filepath.absolute())

    def hashes(self) -> Generator[str, None, None]:
        yield from [f.hash() for f in self._files.values()]
        for d in self._directories.values():
            yield from d.hashes()


def compare_content(d1, d2):
    """
    Returns [0,1] based on content overlap.
    """
    return set(d1.hashes()) == set(d2.hashes())


def compare_depths(d1, d2):
    """
    Returns [0,1] based on the depths of identical files (if present).
    """
    raise NotImplementedError()


def compare_groupings(d1, d2):
    """
    Returns [0,1] based on the relative groupings of identical files (if present).
    """


def compare(d1, d2):
    raise NotImplementedError()
