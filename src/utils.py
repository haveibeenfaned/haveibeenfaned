import pathlib


def save_content(content: str, path: str) -> bool:
    open(path, "w").write(content)
    return file_is_local(path)


def file_is_local(path: str) -> bool:
    return pathlib.Path(path).exists()


def dir_is_local(path: str) -> bool:
    return pathlib.Path(path).is_dir()


def make_unique(inp: list) -> list:
    return list(set(inp))
