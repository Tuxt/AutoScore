
'''
    Extract notes from tunes
    One line per tune
'''

import sys
import argparse

parser = argparse.ArgumentParser(description="Extract abc notes")
parser.add_argument("FILE", help="File to process", nargs="+")
parser.add_argument("-o", "--output", help="Output File", default="output.abc")

args = parser.parse_args()

PREFIX = ['=', '^', '_']
SYMBOLS = ['~', 'H', 'T', '.', '-']

ofile = open(args.output, 'w')

for f in args.FILE:
    print('Processing: ' + f)
    with open(f, 'r') as ifile:
        data = ifile.readlines()

    data_line = ""
    for line in data:

        # Skip empty lines
        if line == "\n":
            continue
        
        # Check new tune header (reset data_line: 1 tune / line)
        if line.startswith('X:'):
            if data_line != "":
                data_line += "\n"
                ofile.write(data_line)
                data_line = ""
            continue

        # Skip header lines
        if line[0].isalpha() and line[1] == ":":
            continue

        # Analize words
        for word in line.split():

            # Check empty
            if word == '':
                continue
            # Check notes
            if word[0] in PREFIX or 'z' in word:
                data_line += word + ' '
            # Check multiplier
            elif word.isdecimal() or '/' in word:
                data_line += word + ' '
            # Check symbols
            elif word in SYMBOLS:
                data_line += word + ' '
            # Check chords
            elif word == '[' or word == ']':
                data_line += word + ' '
            # Check inline header fields (delete)
            elif word.startswith('['):
                #data_line += word + ' '
                continue
            # Check grace notes
            elif word == '{' or word == '}':
                data_line += word + ' '
            # Check (2 (3 ...
            elif word.startswith('('):
                data_line += word + ' '
            # Check for strings
            elif word.startswith('"'):
                #data_line += word + ' '
                continue
            # Check | :| |: || ::
            elif '|' in word or ':' in word:
                continue
            else:
                print("ERROR: Unrecognized word ", word)
                exit(1)


    data_line += '\n'
    ofile.write(data_line)
ofile.close()
exit(0)
            

                
