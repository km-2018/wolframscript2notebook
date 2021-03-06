#!/usr/bin/env python3
import sys

escape_sequences = [r"\:\\", "\n:\\n", '":\\"']
escape_sequences = [s.split(":") for s in escape_sequences]


def parseComment(source):
    lines = [l.strip() for l in source if l.strip()]
    blocks = []
    for line in lines:
        if not line:
            continue
        if line.startswith("###"):
            line = line[3:].strip()
            type = "Subsubsection"
        elif line.startswith("##"):
            line = line[2:].strip()
            type = "Section"
        elif line.startswith("#"):
            line = line[1:].strip()
            type = "Title"
        else:
            type = "Text"
        blocks.append((type, line))
    cells = []
    for type, line in blocks:
        if cells and cells[-1][0] == type:
            cells[-1][1] += "\n" + line
        else:
            cells.append([type, line])
    return cells


def getCells(source):
    source = source.split("\n")
    cells = []
    i = 0
    while i < len(source):
        line = source[i].strip()
        if line == "(*":
            j = i + 1
            while source[j].strip() != "*)":
                j += 1
            cells += parseComment(source[i + 1 : j])
        elif not line:
            j = i
        else:
            j = i
            while j < len(source) and source[j].strip():
                j += 1
            cells.append(("Input", "\n".join(source[i : j + 1])))
        i = j + 1
    return cells


def cell2str(cell):
    def toString(code):
        for r, t in escape_sequences:
            code = code.replace(r, t)
        code = '"' + code + '"'
        return code

    type, line = cell
    type = toString(type)
    line = toString(line)
    if "Input" in type:
        return "Cell[BoxData@RowBox@{" + line + "}," + type + "]"
    return "Cell[" + line + "," + type + "]"


cells = []
for source in sys.argv[1:]:
    code = open(source).read()
    cells.extend(map(cell2str, getCells(code)))
cells = "[{\n" + ",\n".join(cells) + "\n}]"
print(f"Notebook{cells}")
