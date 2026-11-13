from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

from tkinter import filedialog
import itertools
from typing import Final



#TODO: REMOVE FOR RELEASE
#fix single file debugging when working with whole structure
# if not __package__:
#     from sys import path
#     path.insert(0, str(Path(__file__).resolve().parents[3]))
#     __package__ = "openteab.main.lib"
# migrated to __init__ so it can be done on a global level

try:from openteab.globals import *
except:import __init__; from openteab.globals import *

from openteab.main.lib.decorators import *
from openteab.globals import *
from openteab.main.config import DEV_CONFIG as CONFIG, DEV_CONFIG_DIR as CONFIG_DIR
from openteab.main.lib.variable_parse import *


EXTENSIONS_LIST:Final[tuple[str,  ...]] = tuple(''.join(x) for x in itertools.product(*[('o', 'O'), ('t', 'T'), ('j', 'J')]))
'''''';   EXTENSIONS_STRING:Final[ str] = "*." + " *.".join(EXTENSIONS_LIST)
'''''';     UPPER_EXTENSION:Final[ str] = EXTENSIONS_LIST[0].upper()
'''''';             SPACING:Final[ str] = "".join("\\ " for _ in range(30))
'''''';           LINEBREAK:Final[ str] = "\\r\\n"
'''''';                HIDE:Final[bool] = True
'''''';            ENCODING:Final[ str] = "utf-8"
from os.path import join, expanduser
from os import environ; USERPROFILE = environ['USERPROFILE'];del environ
from platform import system as getSystem;IS_WINDOWS = getSystem() == "Windows"; del getSystem
'''''';             DESKTOP:Final[ Path] = Path(join(join(USERPROFILE), 'Desktop') if IS_WINDOWS else join(join(expanduser('~')), 'Desktop'))

def SpecifyOTJ(fileName:str|None=None, EXT:list[str]=EXTENSIONS_LIST, FORCED_SINGLE_FILE:bool=False):
    '''
        Generate Extension filename Variants
        if fileName present, it generates upper and lowercase varaints with combined extensions
        not most the time but a nice to have
        example:
            SpecifyOTJ("cf")
            -> "cf.otj;cf.OTJ;CF.otj;CF.OTJ"
        if fileName is not present it returns EXT (OR default EXTENSIONS_LIST)
    '''
    
    if not fileName:
        return EXTENSIONS_STRING

    #leave this for if per character letter is needed later
    # name_chars = [(char.lower(), char.upper()) if char.isalpha() else (char,) for char in fileName]
    # name_list = [''.join(x) for x in itertools.product(*name_chars)]
    name_list = [''.join(x) for x in (fileName.upper(),fileName.lower())]
    output    = [f"{name}.{ext}" for name in name_list for ext in EXT]
    
    #          v MAGIC CHARACTER BREAK THIS SEQUENCE TO STOP TKINTER APPENDING * TO FILENAMES we want
    if FORCED_SINGLE_FILE:
        #"*.;\\x20"
        return "*\\x2E;\\x20"+(";\\x20".join(output))
    return ";\\x20".join(output)

FileExtentions = [("[Openteab Json] Config.otj", "*\\x2E;\\x20config.otj"),
                  ("[Openteab Json] EXPANDED  ", SpecifyOTJ("config",FORCED_SINGLE_FILE=True))]

def NS(fp, *args, **kw):
    '''
    same as normal json.load except returns a SimpleNamespace object instead of dictionary
    '''
    return json.loads(fp,object_hook=lambda d:SimpleNamespace(**d), *args, **kw)

import tempfile as tmpfs
from os import fsync, fdopen, replace, unlink
class NamespaceEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SimpleNamespace):
            return vars(obj)
        return super().default(obj)
    
@single
class Config:
    def __init__(self):
        import threading
        self.__config_lock = threading.Lock()
        self._json_namespace      = SimpleNamespace()
        self.__config = ""
        pass

    @staticmethod
    def _init():
        pass

    def _save_config(self):
        with self.__config_lock:
            try:
                temp_file, temp_path = tmpfs.mkstemp(dir=str(CONFIG.parent),suffix=".tmp",prefix="config")
                try:
                    COMPACT_CONFIG = tryGetBool(self._json_namespace,"compact_config", False)
                    if COMPACT_CONFIG:
                        with fdopen(temp_file, "wb") as tmp:
                            import gzip
                            dump = json.dumps(self._json_namespace, indent=None,cls=NamespaceEncoder)
                            dump = gzip.compress(dump.encode(ENCODING))
                            print_d(dump)
                            tmp.write(dump)
                            tmp.flush()
                            fsync(tmp.fileno())
                    else:
                        with fdopen(temp_file, "w",encoding=ENCODING) as tmp:
                            tmp.write(json.dumps(self._json_namespace, indent=4, cls=NamespaceEncoder))
                            tmp.write("\n")
                            tmp.flush()
                            fsync(tmp.fileno())
                except OSError as e:
                    print(f"Failed to write temp file, aborting early!")
                    print(f"Failed to save config: {e}")
                    return
                finally:
                    try:
                        replace(temp_path, str(CONFIG))
                    except PermissionError as e:
                        #save to desktop instead, so we don't lose the config but the user will still get a popup saying that there was no permision to write the file
                        replace(temp_path, str(DESKTOP / CONFIG.name))
                        print(f"Config Saved to desktop due to permission exception!")
                        print(f"Failed to save config: {e}")
                    # try: unlink(temp_path)
                    # finally:pass
            except (FileExistsError) as e:
                print(f"Temp file already exists, this should never happen!!")
                print(f"Failed to save config: {e}")
                return
    
    def _load_config(self):
        # self.__import_file_config(CONFIG)
        with self.__config_lock:
            try:
                with open(CONFIG, "rb") as f:
                    tmp = f.read()
                    try:
                        if(DEBUG): self.__config = tmp
                        self._json_namespace = json.loads(tmp, object_hook=lambda d:SimpleNamespace(**d))
                    except Exception as e:
                        print(e)
                        try:
                            import gzip
                            temp_file = CONFIG.parent / "config_decompressed.json"
                            tmp = gzip.decompress(tmp)
                            self._json_namespace = json.loads(tmp, object_hook=lambda d:SimpleNamespace(**d))
                            unlink(temp_file)
                            with open(temp_file, "w") as decomp:
                                decomp.write(json.dumps(self._json_namespace, indent=4, cls=NamespaceEncoder))
                                decomp.write("\n")
                                decomp.flush()
                        except Exception as e:
                            print(f"L2: {e}")
                    finally:
                        return self._json_namespace
            except OSError as e:
                print(f"Failed to load config: {e}")

    def getConfig(self):
        return self._json_namespace

    
    def __import_file_config(self, file_name:Path=None):
        if file_name:
            file_name = filedialog.askopenfilename(initialdir=str(file_name.parent), initialfile=file_name.name,filetypes=FileExtentions,title="Import Config!")
        if not file_name or (isinstance(file_name, str) and not file_name.lower().endswith("config.otj")): return
        with open(file_name, mode='r') as file:
            tmp:str          = file.read(-1)
            if(DEBUG): self.__config    = tmp # we are purposely holding a referece for debugging
            self._json_namespace = json.loads(tmp, object_hook=lambda d:SimpleNamespace(**d))

Config = Config()
c = Config
c._load_config()
c._json_namespace.compact_config = False
c._save_config()
