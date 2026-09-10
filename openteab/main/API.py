#TODO: Add json api calls here including compressed file download from github when file is missing
#           web JSON API CALL example localhost:5555/api/json?file_shorthand
#                              |   or localhost:5555/api/pjson?url_friendly_file_path
#                              v
#                          can be FOUND?
#                              |
#                              |-------- YES ------|
#                              v                   |
#                             NO                   |
#                              |                   |
#                              v                   |
#              request compressed file from github
# "/external_assets/compressed/API/JSON/lang/{lang_code}.gz.b64"
#                              |                   |
#                              v                   |
#                        base64 decode             |
#                              |                   |
#                              v                   |
#                       gzip decompress            |
#                              |                   |
#                              v                   |
#                          save file               |
#                              |                   |
#                              v                   |
#                     send file to client <--------|



#TODO: Move all text into this script for future translations help
#      language code tag used https://docs.sqanit.com/glossary/language-tags/
#      instead of "-" use "_" for better file name scheme
#           web LANG API CALL example localhost:5555/api/lang?lang_code
#                              |
#                              v
#                          can be FOUND?
#                              |
#                              |-------- YES ------|
#                              v                   |
#                             NO                   |
#                              |                   |
#                              v                   |
#              request compressed file from github
# "/external_assets/compressed/API/JSON/lang/{lang_code}.gz.b64"
#                              |                   |
#                              v                   |
#                        base64 decode             |
#                              |                   |
#                              v                   |
#                       gzip decompress            |
#                              |                   |
#                              v                   |
#                          save file               |
#                              |                   |
#                              v                   |
#                     send file to client <--------|
#
#NOTE: we might have to store the encoding somewhere incase we translate for a language not covered by utf-8
#  lang example for en_us.json
#  {
#     "credits": {
#         "originalCreators": "Original Creators",
#         "extra": "Extra Credits",
#         "support": "Support Us",
#         "donators": "Donators Hall of Fame"
#     }
#  }




#NOTE: Why download "FILE.json.gz.b64" instead of just "FILE.json"?
#       To put simply file size, whilst also still being possible for the user
#       to just take the text and decode+decompress it themselves if they don't
#       trust it directly.  
#       for example:
#          you can decode "external_assets\compressed\API\JSON\credits.json.gz.b64"
#          on "https://tools.simonwillison.net/base64-gzip-decoder" and it will return
#          a json minified version of "external_assets\source\API\JSON\credits.json"
#       but do note that being a base64 encode of the normal file means
#       we lose some end file size efficiency, for example the above credits.json
#       source file is 4,883 Bytes, where as the gzip compressed file is 1,065 Bytes
#       but we sacrifice a little bit of file size for ease-of-use enduser decoding
#       that little bit of comfort costs some bytes but typically not as much
#       end file size is 1,420 Bytes ~70.9% reduction in filesize,a loss of
#       ~7.29% over just binary compression
#
#       !@! these are just values based on one file !@!
#       !@! compression effiency can be different depending on the source!@!

#NOTE: Why not store the compressed json instead of the raw one?
#       more or less same reason as above, enduser comfort. We can't hide anything
#       if its completely readable! But also it loads faster if we don't have to
#       decode and decompress at runtime each load

from pathlib import Path
try: from openteab.globals import openteab
except:
    class openteab:from os import getcwd; assets = getcwd() + "/openteab/assets"; cwd = getcwd()
from gzip import decompress
from base64 import b64decode
import json
import requests


ASSETS = Path(openteab.assets)

GithubURL = "https://raw.githubusercontent.com/hybolic/Openteab/Openteab/external_assets/compressed/API/JSON/"


class jtypes_storage:
    class TYPE(str):
        def __new__(self, path):
            instance = super().__new__(self, str(ASSETS / path))
            instance.name = path
            return instance
        
    def __init__(self):
        self.LANG    = jtypes_storage.TYPE("lang")
        self.CREDITS = jtypes_storage.TYPE("")
        self.OTHER   = jtypes_storage.TYPE("")
JSON_TYPES = jtypes_storage()



from io import TextIOWrapper, BufferedReader
class API:
    @staticmethod
    def DecompressData(data:bytes|str|TextIOWrapper|BufferedReader,encoding="utf-8") -> bytes:
        if isinstance(data,(TextIOWrapper, BufferedReader)):
            #if instance is TextIOWrapper or BufferedReader
            #just send it back through with the contents being read
            return API.DecompressData(data.read())
        if isinstance(data,bytes):
            gz = b64decode(data)
        elif isinstance(data,str):
            gz = b64decode(data.encode(encoding))
        else:
            raise TypeError(f"DecompressData can only handle {bytes} or {str} but recieved {type(data)} instead!"); return
        data_bytes = decompress(gz)
        if '\n'.encode(encoding) in data_bytes:
            return data_bytes
        else: #unminify the json
            return json.dumps(json.loads(data_bytes),indent=4).encode(encoding)

    @staticmethod
    def getJsonFile(file:str,type:jtypes_storage.TYPE=JSON_TYPES.OTHER,encoding="utf-8", MINIFY_OUTPUT=False): 
        file_path = Path(type) / file
        if not file_path.exists():
            print(f"file not found \'{file}\', Downloading latest from github!")
            URLS =[ GithubURL + file + ".gz.b54",
                    GithubURL + file.rstrip(".json") + ".gz.b54"]
            for url in URLS:
                print(f"Trying {url}")
                response = requests.get(url,timeout=10)
                if response.ok:
                    file_data = response.content
                    print(f"file found and recieved!")
                    break
            if not response.ok:
                print(f"no file found!")
                return None
            decompressed_data = API.DecompressData(file_data, encoding)
            json_text = decompressed_data.decode(encoding)
            #TODO: async the writer 
            with open(str(file_path) + ".temp", "wb") as outfile:
                outfile.write(decompressed_data)
        else:
            with open(file_path,"r",encoding=encoding) as json_file:
                json_text = json_file.read()
        if MINIFY_OUTPUT:
            json_text = json.dumps(json.loads(json_text),separators=(",",":"))
        return json_text
        
API.getJsonFile("c.json")