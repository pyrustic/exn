import os
import os.path
import sys
from exn.manager import Manager
from exonote import constant, split_target
from exn import utils


HELP_TEXT = """
oooooooooooo      ooooooo  ooooo      ooooo      ooo 
`888'     `8       `8888    d8'       `888b.     `8' 
 888                 Y888..8P          8 `88b.    8  
 888oooo8             `8888'           8   `88b.  8  
 888    "            .8PY888.          8     `88b.8  
 888       o        d8'  `888b         8       `888  
o888ooooood8      o888o  o88888o      o8o        `8  
                                                     

This software is the official Exonote Reader
to read a dossier of interactive notes.

Usage:
    exn
    exn <filename>
    exn <option> [<arg> ...]

Options:
    -b, --build                     Build the index file
    -r, --restrict [<filename>]     Open a note with low restriction
    -R, --Restrict [<filename>]     Open a note with high restriction
    -h, --help                      Show help text

Warning:
    Open a note with restriction when you don't trust the author !
    Low restriction: block the execution of embedded programs.
    High restriction: same as low restriction + block executable links

Tip:
    You can replace a filename with its associated page number !


Visit the webpage: https://github.com/pyrustic/exn
"""


def main():
    args = sys.argv[1:]
    if not args:
        open_exonote()
        return
    first_arg = args[0]
    # open target
    if not first_arg.startswith("-"):
        open_exonote(target=first_arg)
        return
    # build index
    if first_arg in ("-b", "--build") and len(args) == 1:
        build_index()
    # open a note with a low or high restriction
    elif first_arg in ("-r", "--restrict", "-R", "--Restrict"):
        restriction = constant.LOW
        if first_arg in ("-R", "--Restrict"):
            restriction = constant.HIGH
        if len(args) == 1:
            open_exonote(restriction=restriction)
        else:
            open_exonote(target=args[1], restriction=restriction)
    # show the help
    else:
        print(HELP_TEXT)


def open_exonote(target=None, restriction=constant.ZERO):
    if target:
        target = update_target(target)
    dossier = os.getcwd()
    manager = Manager(dossier, restriction)
    manager.start(target)


def build_index():
    dossier = os.getcwd()
    utils.IndexBuilder.build(dossier)
    print("Index successfully built !")


def update_target(target):
    target = target.strip("'\"")
    filename, sid = split_target(target)
    try:
        page = int(filename)
    except (ValueError, TypeError) as e:
        pass
    else:
        filename = get_filename_by_page(page)
    if not filename:
        return
    return filename + sid


def get_filename_by_page(page):
    dossier = os.getcwd()
    index_path = os.path.join(dossier, "index")
    index = utils.IndexParser.parse(index_path)
    if not index:
        return
    try:
        info = index[page - 1]
    except IndexError as e:
        return
    return info.filename


if __name__ == "__main__":
    main()
