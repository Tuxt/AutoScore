
'''
    Fix tie errors on ABC files
    Correct:    note-
    Incorrect:  -note
'''

from tempfile import mkstemp
from shutil import move
from os import fdopen, remove
import argparse

parser = argparse.ArgumentParser(description="Fix tie error on ABC files")
parser.add_argument("FILE", help="File to process", nargs="+")

args = parser.parse_args()

for f in args.FILE:
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(f) as old_file:
            for line in old_file:
                new_file.write(line.replace(" -", "- "))
    
    remove(f)
    move(abs_path, f)
