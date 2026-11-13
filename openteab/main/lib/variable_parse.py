from collections.abc import Iterable

def tryGetStr(raw,key:str,default:str|None=None):
    return ParseStr(getattr(raw,key,None),default)
def ParseStr(parse,default):
                          # v int and bool are same so only need to define one
    if isinstance(parse,(str,int,float)):
        # this part is not needed as str(bool) outputs True or False already
        # but i'll leave it as a reference
        # if isinstance(out, bool):
        #     return "True" if out else "False"
        return str(parse)
    return default

def tryGetInt(raw,key:str,default:int=0):
    return ParseInt(getattr(raw,key,None),default)
def ParseInt(parse, default):
    try:
        return int(parse)
    except (ValueError, TypeError, AttributeError):
        return default

def tryGetFloat(raw,key:str,default:float=0.0):
    return ParseFloat(getattr(raw,key,None),default)
def ParseFloat(parse, default):
    try:
        return float(parse)
    except (ValueError, TypeError, AttributeError):
        return default
                

def tryGetBool(raw,key:str,default:bool=False):
    return ParseBool(getattr(raw,key, None),default)
def ParseBool(parse,default:bool=False):
    if isinstance(parse, bool):
        return parse
    elif isinstance(parse, str):
        parse_lower = parse.strip().lower()
        if   parse_lower in ("1", "true", "yes", "y"):
            return True
        elif parse_lower in ("0", "false", "no", "n"):
            return False
    elif isinstance(parse, (int,float)):
        return abs(parse) >= 1
    return default

def tryGetListLike(raw,key:str,default:list=None):
    return ParseListLike(getattr(raw,key,None),default)
def ParseListLike(parse,default):
    if isinstance(parse, Iterable) and not isinstance(parse, (str, bytes, bytearray)):
        return parse
    return default

def ParseToNamepsace(obj):
    from types import SimpleNamespace
    def parse(data):
        if type(data) is list:
            return list(map(parse, data))
        elif type(data) is dict:
            sns = SimpleNamespace()
            for key, value in data.items():
                setattr(sns, key, parse(value))
            return sns
        else:
            return data
    return parse(obj)