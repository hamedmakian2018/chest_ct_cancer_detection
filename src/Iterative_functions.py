from pathlib import Path


def mk_dir(name):
    Dir_name = Path(name)
    Dir_name.mkdir(parents=True, exist_ok=True)
    return Dir_name
