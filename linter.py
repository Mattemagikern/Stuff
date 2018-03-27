#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This python linter will check:
    that no line exceeds 80 chars,
    that no line contains singlequotes
    that no line contains tabs
    that all single arithmetic operands are surrounded by whitespaces
    that all double arithmetic operands are surrounded by whitespaces
    that all commas are followed by a whitespace.

It will print out all violations of this code standard. 
"""
import sys
import os
import re
import py_compile
from termcolor import colored

path = "."
EXITCODE = 0
ERRORS= []
operands = (["!", "|", "*", "/", "+", "-", "=", "<", ">",
            "^", "%"])
keywords = ["True", "False", "Exception", "None", "Popen", "import"]

def test_compile(f):
    """
    Tests if a python file contans a syntax error
    """
    try:
        py_compile.compile(f, doraise = True)
    except py_compile.PyCompileError, e:
        print colored(f,"white"), colored(": won't compile, ","red")
        print colored(e,"cyan")
        return False
    return True

def check_80char(line, nbr):
    """
    checks if a string in the exceeds 80 chars
    """
    if len(line) > 80:
        text = "line > 80 char"
        ERRORS.append((text, line, nbr))
        return False
    return True

def tab(line, nbr):
    """
    Checks if a string contains tabs
    """
    if "\t" in line:
        text = "contains tab"
        ERRORS.append((text, line, nbr))
        return False
    return True

def trailing_whitespace(line, nbr):
    """
    checks if a string ends with a whitespace
    """
    if line[-2] == " ":
        text = "trailing_whitespace"
        ERRORS.append((text, line, nbr))
        return False
    return True

def single_quote(line, nbr):
    """
    checks if a ' exists in a string
    """
    if "'" in line:
        text = "single quote"
        ERRORS.append((text, line, nbr))
        return False
    return True


def camelCase(line, nbr):
    """
    checks if a string contains camesCase
    """
    if (line != line.lower() and line != line.upper() and
        not any([x in line for x in keywords])):
        text = "CamelCase"
        ERRORS.append((text, line, nbr))
        return False
    return True

def commas(line, nbr):
    """
    checks that all commas are followed by a whitespace. 
    """
    commas = [pos for pos,char in enumerate(line) if char == ","]
    for comma in commas:
        if (line[comma+1] != "\n" and line[comma+1] != " "):
            ERRORS.append(("Comma",line,nbr))
            return False
    return True

def single_operand(line, indexes, nbr):
    """
    checks if all single arithmetic operations are surrounded by whitespace
    """
    for index in indexes:
        if(line[index-1] != " " and
                line[index+1] != " " and line[index] != "-"):
            ERRORS.append(("single_operand", line, nbr))
            return False
    return True

def double_operand(line, indexes, nbr):
    """
    checks if all double operands (++, --, +=, <<) are surrounded with
    whitespaces
    """
    for index in indexes:
        if (line[index-1] != " " and line[index+2] != " " and
            line[index:index+2] != "**"):
            ERRORS.append(("double_operand", line, nbr))
            return False
    return True

def print_errors(f):
    """
    prints all Errors found in a file
    """
    global ERRORS, EXITCODE
    if len(ERRORS) > 0:
        EXITCODE = 1
    for e in ERRORS:
        print colored(f,"white"),"::", colored(e[0],"red"), ":", \
        colored(e[2],"blue"), ":", colored(e[1][:-1],"white")
    ERRORS = []


def test_file(f):
    """
    tests a file if it follows the linting
    """
    with open(f, "r") as f:
        line_nbr = 0
        flag = True
        for line in f:
            line_nbr += 1
            line = line.strip(" ").replace("\t", "")
            if line.strip()[:3] == '"""':
                flag = not flag
                continue
            if (len(line) > 1 and line[0] != "#" and
                    line[:2] != "//" and line[0] != "*" and
                    "if __name__ == '__main__':" not in line and flag):
                check_80char(line, line_nbr)
                tab(line, line_nbr)
                trailing_whitespace(line, line_nbr)
                line = re.sub('".*?"', '""', line)
                single_quote(line, line_nbr)
                commas(line, line_nbr)
                double_indexes = [i[0] for i in enumerate(zip(line,line[1:]))
                        if i[1][0] in operands and i[1][1] in operands]
                single_indexes = [i[0] for i in enumerate(zip(line,line[1:])) if
                    i[1][0] in operands and i[1][1] not in operands and i[0]-1
                    not in double_indexes]
                double_operand(line, double_indexes, line_nbr)
                single_operand(line, single_indexes, line_nbr)
                line = re.sub("\[.*?\]", "[]", line)
                line = re.sub(r'\s*#.*', '', line)
                camelCase(line, line_nbr)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        path = sys.argv[1]
    file_list = []
    for root, directories, files in os.walk(path):
        for filename in files:
            if (filename.endswith(".py") and filename !=
                "code_check.py"):
                filepath = os.path.join(root, filename)
                file_list.append(filepath)

    for f in file_list:
        if test_compile(f):
            test_file(f)
            print_errors(f)

    for root, directories, files in os.walk(path):
        for filename in files:
            if filename.endswith(".pyc"):
                os.remove(os.path.join(root, filename))
    sys.exit(EXITCODE)
