from gzip import decompress, compress
from base64 import b64encode, b64decode
from pathlib import Path
from os import getcwd
import json
COMPRESSION_LOG = Path(getcwd(), "external_assets", "Compression.log")
COMPRESSION_LOG.unlink(missing_ok=True)

source          = Path(getcwd(), "external_assets", "source")
destination     = Path(getcwd(), "external_assets", "compressed")
assets          = Path(getcwd(), "openteab", "assets")
test            = Path(getcwd(), "external_assets", "test")
encoding = "utf-8"
import time
with open(COMPRESSION_LOG, "w", encoding="utf-8") as outfile:
    outfile.write(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
    APP_START = time.perf_counter_ns()
    for fileOrFolder in source.rglob("*"):
        if fileOrFolder.is_file():
            start = time.perf_counter_ns()
            with open(fileOrFolder, "r", encoding=encoding) as f:
                assets_file = assets / fileOrFolder.relative_to(source / "API" / "JSON")
                print(assets_file)
                assets_file.unlink(missing_ok=True)
                if fileOrFolder.suffix == ".json":
                    raw = f.read()
                    with open(assets_file, "w", encoding=encoding) as asset_file:
                        asset_file.write(raw)
                    json_object = json.loads(raw)
                    data_unmini = len(raw.encode(encoding))
                    data = json.dumps(json_object,separators=(",",":"))
                else:
                    data_unmini = None
                    data = f.read()
                    with open(assets_file, "w", encoding=encoding) as asset_file:
                        asset_file.write(data)
                __encoded_data = data.encode(encoding)
                data_gzip = compress(__encoded_data)
                data_b64  = b64encode(data_gzip).decode(encoding)
                delta = time.perf_counter_ns() - start

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
                    
            text_data = [
                f"File:      {fileOrFolder.name}",
                f"Size:      {size_ref:,} B",
                f"GZip:      {size_comp:,} B",
                f"Base64:    {size_b64:,} B",
                f"Reduction: {(1-size_b64/size_ref) * 100:.1f}% [{0-dif:,} B]",
                f"PASS:      {data == data_r}",
                f"Time:      {delta // 1000000000}s {(delta // 1000000) % 1000}ms {delta % 1000000}ns",
                "","","",
            ]
            outfile.write("\n".join(text_data))
            print("\n".join(text_data))
    DETLA = time.perf_counter_ns() - APP_START
    print(f"Total Time:      {DETLA // 1000000000}s {(DETLA // 1000000) % 1000}ms {DETLA % 1000000}ns")
    outfile.write(f"Total Time:      {DETLA // 1000000000}s {(DETLA // 1000000) % 1000}ms {DETLA % 1000000}ns")