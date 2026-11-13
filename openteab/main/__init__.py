if not __package__:
    from sys import path
    from pathlib import Path
    path.insert(0, str(Path(__file__).resolve().parents[2]))
    __package__ = "openteab.main"
    del path, Path
    
from .core import BiomeTracker

__all__ = ["BiomeTracker"]