from __future__ import annotations
from typing import Any, get_args, Literal, Final
from abc import ABC, abstractmethod
import platform as _platform




def OCRBase(ABC):
    @property
    def CURRENT_INSTANCE() -> OCRBase|None:
        return list(OCRBase.__INSTANCES)[0] if len(OCRBase.__INSTANCES) > 0 else None
    __INSTANCES:dict[OCRBase]=dict()
    pass