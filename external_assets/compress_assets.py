from time import perf_counter_ns, strftime, gmtime
APP_START = perf_counter_ns()

from gzip import decompress, compress
from base64 import b64encode, b64decode
from pathlib import Path
from os import getcwd, getenv
from json import loads, dumps
from sys import path

COMPRESSION_LOG = Path(getcwd(), "external_assets", "Compression.log")
COMPRESSION_LOG.unlink(missing_ok=True)
encoding = "utf-8"

with open(COMPRESSION_LOG, "w", encoding=encoding) as outfile:

    source          = Path(getcwd(), "external_assets", "source")
    destination     = Path(getcwd(), "external_assets", "compressed")
    assets          = Path(getcwd(), "openteab", "assets")


    outfile.write(strftime("%Y-%m-%d %H:%M:%S", gmtime())+"\n")
    delta_out = []
    text_out = []
    for fileOrFolder in source.rglob("*"):
        if fileOrFolder.is_file():
            start = perf_counter_ns()
            with open(fileOrFolder, "r", encoding=encoding) as f:
                assets_file = assets / fileOrFolder.relative_to(source / "API" / "JSON")
                print(assets_file)
                assets_file.unlink(missing_ok=True)
                if fileOrFolder.suffix == ".json":
                    raw = f.read()
                    with open(assets_file, "w", encoding=encoding) as asset_file:
                        asset_file.write(raw)
                    json_object = loads(raw)
                    data_unmini = len(raw.encode(encoding))
                    data = dumps(json_object,separators=(",",":"))
                else:
                    data_unmini = None
                    data = f.read()
                    with open(assets_file, "w", encoding=encoding) as asset_file:
                        asset_file.write(data)
                __encoded_data = data.encode(encoding)
                data_gzip = compress(__encoded_data)
                data_b64  = b64encode(data_gzip).decode(encoding)
                delta = perf_counter_ns() - start

                size_precomp = len(__encoded_data)
                size_comp    = len(data_gzip)
                size_b64     = len(data_b64.encode(encoding))
                size_ref     = data_unmini if data_unmini != None else size_precomp
                dif          = size_ref - size_b64

                dest = destination / (fileOrFolder.relative_to(source))
                dest.parent.mkdir(parents=True,exist_ok=True)

                with open(dest.with_suffix(".gz.b64"), "w", encoding=encoding) as o:
                    o.write(data_b64)

                data_b64_r  = data_b64
                data_gzip_r = b64decode(data_b64_r)
                data_r      = decompress(data_gzip_r).decode(encoding)
                    
            text_out.append([
                f"File:      {fileOrFolder.name}",
                f"Size:      {size_ref:,} B",
                f"GZip:      {size_comp:,} B",
                f"Base64:    {size_b64:,} B",
                f"Reduction: {(1-size_b64/size_ref) * 100:.1f}% [{0-dif:,} B]",
                f"PASS:      {data == data_r}",
                f"Time:      {delta // 1000000000}s {(delta // 1000000) % 1000}ms {delta % 1000000}ns",
                "","","",
            ])
            delta_out.append(delta)


    start = perf_counter_ns()
    # print("Export openteab and roblox to Frontend/Public")


    parent_dir:Path = Path(__file__).resolve().parent
    PROJECT_ROOT = Path.cwd()

    if parent_dir.name == "external_assets" and (parent_dir.parent / "openteab").is_dir():
        PROJECT_ROOT = parent_dir.parent
        path.insert(0, str(PROJECT_ROOT))

    from openteab.globals import roblox, openteab


    def serialize_object(instance):
        if instance is None:
            return "None"
        
        #make path relative to project root
        if isinstance(instance, Path):
            try: return str(instance.relative_to(PROJECT_ROOT)).replace("\\","/")
            except:
                try: return "%LOCALAPPDATA%/" + str( instance.relative_to(getenv("LOCALAPPDATA"))).replace("\\","/")
                except: return str(instance).replace("\\","/")

        
        if isinstance(instance, (str, int, float, bool)):
            return instance
        
        if isinstance(instance, dict):
            return {
                str(key): serialize_object(value)
                for key, value in instance.items()
            }
        
        if isinstance(instance, (list, tuple, set)):
            return [serialize_object(value) for value in instance]
        
        # Class instance
        if hasattr(instance, "__dict__"):
            output = {}
            for key, value in vars(instance).items():
                if not key.startswith("__"):
                    output[key] = serialize_object(value)
            for key, value in vars(type(instance)).items():
                if key.startswith("__") or (key in output) or (callable(value) and not isinstance(value, type)):
                    continue
                output[key] = serialize_object(value)
            return output

        return str(instance)



    rbx   = dumps(serialize_object(roblox),indent=4)
    opntb = dumps(serialize_object(openteab),indent=4)

    with open("openteab/frontend/public/json/roblox.json",'w') as file:
        file.write(rbx)
    with open("openteab/frontend/public/json/openteab.json",'w') as file:
        file.write(opntb)
    delta = perf_counter_ns() - start
    
    #OUTPUT STUFF
    DETLA = perf_counter_ns() - APP_START
    delta_out = sum(delta_out)

    out=[]
    for val in text_out: out.append("\n".join(val))
    out = "\n".join(out)
    outfile.write(out)
    print(f"Python Object FileOut:    {delta // 1000000000}s {(delta // 1000000) % 1000}ms {delta % 1000000}ns\n\n\n")
    outfile.write(f"Python Object FileOut:      {delta // 1000000000}s {(delta // 1000000) % 1000}ms {delta % 1000000}ns\n\n\n\n")
    print(out)
    print(f"Process Time:    {delta_out // 1000000000}s {(delta_out // 1000000) % 1000}ms {delta_out % 1000000}ns")
    outfile.write(f"Process Time:      {delta_out // 1000000000}s {(delta_out // 1000000) % 1000}ms {delta_out % 1000000}ns\n")
    print(f"Total Time:      {DETLA // 1000000000}s {(DETLA // 1000000) % 1000}ms {DETLA % 1000000}ns")
    outfile.write(f"Total Time:        {DETLA // 1000000000}s {(DETLA // 1000000) % 1000}ms {DETLA % 1000000}ns")