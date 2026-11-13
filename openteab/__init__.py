if not __package__:
    from sys import path
    from pathlib import Path
    path.insert(0, str(Path(__file__).resolve().parents[1]))
    __package__ = "openteab"
    del path, Path