import re
import os
import sys
import latexcodec
from PySide6.QtWidgets import QApplication, QMessageBox

def must_omit(i):
    return re.match("comment", i) or re.match("%%", i)

def parse_bibfile(file):
    try:
        #with open(file, "r", encoding="utf8") as f:
        with open(file, "r", encoding="latin1") as f:
            text = f.read()
    except FileNotFoundError:
        QMessageBox.warning(
                None, "Missing BibTex file",
                "The file '%s' can't be found!\nUsage: BibTexExplorer FILE.bib"%file,
            )
        sys.exit(1)

    entries = {}

    entry_blocks = [i for i in re.split("\n@", text) if not must_omit(i)]

    if entry_blocks[0][0] == "@":
        entry_blocks[0] = entry_blocks[0][1:]

    for entry in entry_blocks:
        entry_dict = {}
        i1 = re.match("(?P<type>.*){(?P<key>.*),", entry)
        if i1:
            entry_dict["key"] = i1.group("key")
            entry_dict["type"] = i1.group("type")

        items = ["doi", "journal"]
        itemslatex = ["author", "title"]
        itemsspecial = ["year", "citations"]
        # for i in items+itemsspecial+itemslatex:
        #     i2 = re.search("\s*%s\s*=\s*{?(?P<%s>\S.*)\S}?\S?" % (i, i), entry)
        #     if i2:
        #         if i in itemslatex:
        #             entry_dict["%s" % i] = i2.group("%s" % i).replace("{","").replace("}","").encode("utf-8").decode("latex+latin1")
        #         else:
        #             entry_dict["%s" % i] = i2.group("%s" % i)
        #     else:
        #         entry_dict["%s" % i] = ""
        for i in items:
            i2 = re.search("\s*%s\s*=\s*{(?P<%s>\S.*)},\n" % (i, i), entry)
            if i2:
                entry_dict["%s" % i] = i2.group("%s" % i)
            else:
                i2 = re.search("\s*%s\s*=\s*{(?P<%s>\S.*)}\n" % (i, i), entry)
                if i2:
                    entry_dict["%s" % i] = i2.group("%s" % i)

        for i in itemslatex:
            i2 = re.search("\s*%s\s*=\s*{(?P<%s>\S.*)},\n" % (i, i), entry)
            if i2:
                entry_dict["%s" % i] = i2.group("%s" % i).replace("{","").replace("}","").encode("utf-8").decode("latex+latin1")
            else:
                i2 = re.search("\s*%s\s*=\s*{(?P<%s>\S.*)}\n" % (i, i), entry)
                if i2:
                    entry_dict["%s" % i] = i2.group("%s" % i).replace("{","").replace("}","").encode("utf-8").decode("latex+latin1")

        for i in itemsspecial:
            i2 = re.search("\s*%s\s*=\s*(?P<%s>\S.*),\n" % (i, i), entry)
            if i2:
                entry_dict["%s" % i] = i2.group("%s" % i).replace("{","").replace("}","")
            else:
                i2 = re.search("\s*%s\s*=\s*(?P<%s>\S.*)\n" % (i, i), entry)
                if i2:
                    entry_dict["%s" % i] = i2.group("%s" % i).replace("{","").replace("}","")

        if entry_dict != {}:
            entry_dict["bibtex"] = entry
            entries[entry_dict["key"]]=entry_dict

    return entries
