import ast
import os
from pathlib import Path
from typing import Any, List

from base92 import Base92Alpha, Base92

USER_PATH = ""

from datetime import datetime
from tzlocal import get_localzone

class ManifestGenerator:
    def __init__(self, NAME:str, CLASS:type, REQUIRES:list[str|tuple[str,str]], file:str|Path, Author:str|List[str]="", Description:str|List[str]=""):
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
            Description = Description.splitlines() if "\n" in Description else [Description]
        self.Description:str|List[str]= Description
        self.DateGenearted:str = datetime.now(get_localzone()).strftime("%d/%m/%Y %H:%M %Z%z")

    def GetHash(self, encoder:Base92Alpha=Base92.BACKSLASH):
        with open(self.__FILE, 'r') as file:
            source = file.read()
        tree = ast.parse(source)
        line_numbers = set()
        target_class_name = self.Class
        BIGGER_SELF = self
        class LineInspector(ast.NodeVisitor):
            def visit_Import(self, node):
                for alias in node.names:
                    if alias.name in BIGGER_SELF.Requirements:
                        start = node.lineno
                        end = getattr(node, 'end_lineno', node.lineno)
                        line_numbers.update(range(start, end + 1))
                self.generic_visit(node)

            def visit_ImportFrom(self, node):
                module = node.module or ""
                for alias in node.names:
                    full_import = f"{module}.{alias.name}" if module else alias.name
                    if alias.name in BIGGER_SELF.Requirements or full_import in BIGGER_SELF.Requirements or module in BIGGER_SELF.Requirements:
                        start = node.lineno
                        end = getattr(node, 'end_lineno', node.lineno)
                        line_numbers.update(range(start, end + 1))
                self.generic_visit(node)

            def visit_ClassDef(self, node):
                if node.name == target_class_name:
                    start = node.lineno
                    end = getattr(node, 'end_lineno', node.lineno)
                    line_numbers.update(range(start, end + 1))
                self.generic_visit(node)

        LineInspector().visit(tree)
        FILTER= [""]
        import re
        REGEX_COMMENT_BLOCK1 = re.compile(r'("""[^"]*?""")')
        REGEX_COMMENT_BLOCK2 = re.compile(r"('''[^']*?''')")
        SPECIAL_CASE = re.compile(r"(?<!['\"])(?:['\"]){1,2}(?!['\"])")
        REGEX_COMMENT_LINE   = re.compile(r"(#.*$)")
        REGEX_HINTS_AND_DECO = re.compile(r"(^@.*$)")
        source_lines = source.splitlines()
        Lines: List[str] = [
            processed
            for line_index in sorted(line_numbers)
            if 0 < line_index <= len(source_lines)
            if (processed := source_lines[line_index - 1].replace(" ", "")) not in FILTER
            if not REGEX_HINTS_AND_DECO.search(processed := source_lines[line_index - 1].replace(" ", ""))
            if not SPECIAL_CASE.search(processed := source_lines[line_index - 1].replace(" ", ""))
        ]
        New_Lines = []
        for line_index in range(len(Lines)):
            if REGEX_COMMENT_LINE.search(Lines[line_index]):
                NEW_LINE = REGEX_COMMENT_LINE.sub("",Lines[line_index])
                if NEW_LINE not in FILTER:
                    New_Lines.append(NEW_LINE)
            else:
                New_Lines.append(SPECIAL_CASE.sub("",Lines[line_index]))
        Lines = New_Lines
                    
        
        import hashlib
        encoding = encoder.GetEncoding()
        line = "".join(Lines)
        line = REGEX_COMMENT_BLOCK1.sub("",line)
        line = REGEX_COMMENT_BLOCK2.sub("",line)
        line = line.encode(encoding)
        bytes_ = hashlib.sha512(line).digest()
        
        return Base92.EncodeString(bytes_, encoder)