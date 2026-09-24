import ast
import os
from pathlib import Path
from typing import Any, Final, List, Protocol, Type, runtime_checkable
import inspect
                    
        
import hashlib

from base92 import Base92Alpha, Base92

USER_PATH = ""
NO_TEXT :Final[str]  = ""
SPACE   :Final[str]  = " "
NEW_LINE:Final[str]  = "\n"

from datetime import datetime
from tzlocal import get_localzone

class REGEX:
    from re import Pattern as __Pattern
    import re as __re

    @staticmethod
    def __COMPILE_REGEX(str, compiler=__re.compile) -> __Pattern:
        return compiler(str)
    
    COLAPSE        = __COMPILE_REGEX(r'([\s\S]*?)\[\s*\n\s*([^\[\]]*?)\s*\n\s*\]')

    NEW_LINE_ARRAY = __COMPILE_REGEX(r'\n\s*(?=\[)')
    NEW_LINE_DICT  = __COMPILE_REGEX(r'\n\s*(?=\{)')

    REQUIREMENTS   = __COMPILE_REGEX(r'("Requirements": \[\s*\n)([\s\S]*?)(\s*\])')
    NOT_SAFE_CHAR  = __COMPILE_REGEX(r'[^a-zA-Z0-9 _.-]')
    SPACE_LIKE     = __COMPILE_REGEX(r'\s+')

    del __re, __Pattern, __COMPILE_REGEX


class ManifestData:
    def __init__(self, NAME:str, CLASS:type, REQUIRES:list[str|tuple[str,str]], file:str|Path, Author:str|List[str]=NO_TEXT, Description:str|List[str]=NO_TEXT):
        self.Name:str               = NAME
        self.Class:str              = CLASS.__name__
        self.BaseClass              = CLASS.__base__.__name__ if CLASS.__base__ else "None"
        self.Requirements:list[str|tuple[str,str]] = REQUIRES
        if(isinstance(file,str)):
            self.__FILE             = file
            self.FILE               = Path(file).name
        else:
            self.__FILE             = str(file)
            self.FILE               = file.name
        self.Hash:str               = self.GetHash()
        if isinstance(Author,str):
            Author = [Author]
        self.Author:str|List[str]   = Author
        if isinstance(Description,str):
            Description = Description.splitlines() if NEW_LINE in Description else [Description]
        self.Description:str|List[str]= Description
        self.DateGenearted:str = datetime.now(get_localzone()).strftime("%d/%m/%Y %H:%M %Z%z")

    def GetJson(self, indents=4):
        import json
        #this lambda just removes private and mangled variables from the input variable
        filter = lambda obj:{name:value for name, value in obj.__dict__.items() if not name.startswith('_')}

        #if we have indenting, we do the special formating
        if indents > 0:
            text = json.dumps(self,default=filter,indent=4)
            def collapse_array(match):
                prefix = match.group(1)
                #if its Author or Description we just exit early
                if "Author" in prefix or "Description" in prefix:
                    return match.group(0)
    
                content = match.group(2)

                #compact the content to just ["import","stuff"]
                compact_content = NO_TEXT.join(line.strip() for line in content.splitlines())
                return f"{prefix}[{compact_content}]"
            
            #yes we are essentially just collapsing some stuff to make it neat
            collapsed =  REGEX.COLAPSE.sub(collapse_array,text)
            #run the requirements compaction                     | this long thing here just handle spacing properly for requirements                |
            return REGEX.REQUIREMENTS.sub(lambda m: m.group(1) + (SPACE * (indents * 2)) + REGEX.NEW_LINE_ARRAY.sub(NEW_LINE.ljust(indents * 2, SPACE), m.group(2)).strip() + m.group(3), collapsed)
        #else we just output the default dumps with 0 indent
        #also known as minified json
        return json.dumps(self,default=filter, indent=indents)

    def WriteManifest(self):
        from pathlib import Path
        import unicodedata
        NAME = "M_" + REGEX.SPACE_LIKE.sub('_', REGEX.NOT_SAFE_CHAR.sub(NO_TEXT, unicodedata.normalize('NFKD', self.Name)).strip(' .'))[:(24-7)] + ".json"
        file_path = Path(self.__FILE).parent / NAME
        with open(file_path, 'w') as file:
            file.write(self.GetJson())
        return file_path.exists()

    def GetHash(self, encoder:Base92Alpha=Base92.BACKSLASH):
        try:
            with open(self.__FILE, 'r') as file:
                source = file.read()
            tree = ast.parse(source)
            line_numbers = set()
            target_class_name = self.Class
            BIGGER_SELF = self
            class LineInspector(ast.NodeVisitor):
                def __init__(self):
                    self.line_numbers = set()
                    self.used_identifiers = set()
                    self.imports_map = {}
                    self.in_target_class = False

                def visit_ClassDef(self, node):
                    if node.name == target_class_name:
                        #capture class lines (including decorators)
                        start = node.lineno
                        end = getattr(node, "end_lineno", node.lineno)
                        self.line_numbers.update(range(start, end + 1))

                        #step into the class context to track usage
                        self.in_target_class = True
                        self.generic_visit(node)
                        self.in_target_class = False
                    else:
                        self.generic_visit(node)

                def visit_Name(self, node):
                    if self.in_target_class:
                        self.used_identifiers.add(node.id)
                        self.generic_visit(node)

                def visit_Attribute(self, node):
                    if self.in_target_class:
                        current = node
                        while isinstance(current, ast.Attribute):
                            current = current.value
                        if isinstance(current, ast.Name):
                            self.used_identifiers.add(current.id)
                    self.generic_visit(node)

                def visit_Import(self, node):
                    for alias in node.names:
                        name = alias.asname if alias.asname else alias.name
                        self.imports_map[name] = node
                        #Also map root module 'os.path' maps to 'os'
                        self.imports_map[name.split(".")[0]] = node
                    self.generic_visit(node)

                def visit_ImportFrom(self, node):
                    module = node.module or NO_TEXT
                    if module:
                        self.imports_map[module.split(".")[0]] = node
                    for alias in node.names:
                        name = alias.asname if alias.asname else alias.name
                        self.imports_map[name] = node
                    self.generic_visit(node)

            builder = LineInspector()
            builder.visit(tree)

            #build final line numbers by combining target class lines and matched imports
            line_numbers = set(builder.line_numbers)
            raw_requirements = set()

            for ident in builder.used_identifiers:
                if ident in builder.imports_map:
                    imp_node = builder.imports_map[ident]
                    start = imp_node.lineno
                    end = getattr(imp_node, "end_lineno", imp_node.lineno)
                    line_numbers.update(range(start, end + 1))

                    if isinstance(imp_node, ast.Import):
                        for alias in imp_node.names:
                            raw_requirements.add(alias.name.split(".")[0])
                    elif isinstance(imp_node, ast.ImportFrom):
                        mod = imp_node.module or NO_TEXT
                        if mod:
                            raw_requirements.add(mod.split(".")[0])

            built_requirements = []
            import importlib
            for pkg in raw_requirements:
                try:
                    #query environment for the actual installed version
                    ver = importlib.metadata.version(pkg)
                    built_requirements.append([pkg, ver])
                except importlib.metadata.PackageNotFoundError:
                    #fallback if package isn't pip-installed or is part of standard library
                    built_requirements.append([pkg])

            self.Requirements = built_requirements

            FILTER= [NO_TEXT, "\r", NEW_LINE, "\r\n", "\n\r"]#no text and various newlines
            import re
            REGEX_COMMENT_BLOCK1 = re.compile(r'("""[^"]*?""")') # """
            REGEX_COMMENT_BLOCK2 = re.compile(r"('''[^']*?''')") # '''
            SPECIAL_CASE = re.compile(r"(?<!['\"])(?:['\"]){1,2}(?!['\"])") #ignores "" and " on their own
            REGEX_COMMENT_LINE   = re.compile(r"(#.*$)") #comment and everything after
            REGEX_HINTS_AND_DECO = re.compile(r"(^@.*$)") #decorators
            source_lines = source.splitlines()
            Lines: List[str] = [
                processed
                for line_index in sorted(line_numbers)
                if 0 < line_index <= len(source_lines) #line is longer then 0
                #we do a whole ton of filtering here
                if (processed := source_lines[line_index - 1].replace(SPACE, NO_TEXT)) not in FILTER
                if not REGEX_HINTS_AND_DECO.search(processed := source_lines[line_index - 1].replace(SPACE, NO_TEXT))
                if not SPECIAL_CASE.search(processed := source_lines[line_index - 1].replace(SPACE, NO_TEXT))
            ]
            New_Lines = []
            for line_index in range(len(Lines)):
                if REGEX_COMMENT_LINE.search(Lines[line_index]):
                    _NEW_LINE = REGEX_COMMENT_LINE.sub(NO_TEXT,Lines[line_index])
                    if NEW_LINE not in FILTER:
                        New_Lines.append(_NEW_LINE)
                else:
                    New_Lines.append(SPECIAL_CASE.sub(NO_TEXT,Lines[line_index]))
            Lines = New_Lines

            encoding = encoder.GetEncoding()
            line = REGEX_COMMENT_BLOCK2.sub(NO_TEXT,REGEX_COMMENT_BLOCK1.sub(NO_TEXT,NO_TEXT.join(Lines))).encode(encoding)
            bytes_ = hashlib.sha512(line).digest() #not the fastest hash but will give us a fixed length long hash for Base92
            
            return Base92.EncodeString(bytes_, encoder)
        except Exception as e:
            print (f"{e}")
            return f"{encoder.NAME}:"


def Manifest(Name:str=NO_TEXT,Author:str|List[str]=NO_TEXT, Description:str|List[str]=NO_TEXT):
    #gives anything with @Manifest the getManifest function
    #used mostly so we have a way in vscode to get it to
    #show up with intellisense
    @runtime_checkable
    class HasManifest(Protocol):
        @classmethod
        def getManifest(cls) -> ManifestData: ...
        
    def decorator(cls:Type) -> Type[HasManifest]:
        try:
            file_name = inspect.getsourcefile(cls) or inspect.getfile(cls)
        except:
            file_name = None
        finally:
            if not file_name:
                file_name = "NoFileFound"
        RegisterdName = Name if isinstance(Name,str) and len(Name) > 3 else cls.__name__
        data = ManifestData(RegisterdName, cls,
                            [[NO_TEXT]], #done during GetHash()
                            file_name, Author, Description)
        ManifestRegistry.Register(data,RegisterdName)
        #store manifest on the class
        cls._MANIFEST = data
        #give user a way to call it
        cls.getManifest = classmethod(lambda _cls: _cls._MANIFEST)
        return cls #type: ignore
    return decorator

class ManifestRegistry:
    __ManifestRegistry = dict()

    class DuplicateRegistryError(ValueError):
        """Raised when trying to register a duplicate name."""
        pass

    @classmethod
    def Register(cls, manifest:ManifestData, Name:str):
        if Name in cls.__ManifestRegistry.keys():
            raise cls.DuplicateRegistryError(f"{Name} Already registered!")
        cls.__ManifestRegistry.update({Name:manifest})

    @classmethod
    def GetRegistry(cls):
        return cls.__ManifestRegistry.copy()

if False:
    #TESTING THE OUTPUT FOR @Manifest
    import autoit

    @Manifest()
    class Test(ManifestRegistry):
        """
        BLOCK COMMENT
        """
        @staticmethod
        def func(str): #INLINE COMMMENT
            autoit.send("")

    print(Test.getManifest().GetJson())

    #output all manifests
    for i,v in ManifestRegistry.GetRegistry().items():
        data:ManifestData = v
        print(data.GetJson())