
'''
    Fix or delete decorators
    !roll!          -> ~
    ~               -> [Ok]
    !fermata!       -> H
    H               -> [Ok]
    !accent!        -> [Delete]
    L               -> [Delete]
    !lowermordent!  -> [Delete]
    M               -> [Delete]
    !uppermordent!  -> [Delete]
    P               -> [Delete]
    !coda!          -> [Delete]
    O               -> [Delete]
    !segno!         -> [Delete]
    S               -> [Delete]
    !trill!         -> T
    T               -> [Ok]
    !upbow!         -> [Delete]
    u               -> [Delete]
    !downbow!       -> [Delete]
    v               -> [Delete]
    .               -> [Ok]
    -               -> [Ok]
'''

import argparse

parser = argparse.ArgumentParser(description="Fix tie error on ABC files")
parser.add_argument("FILE", help="File to process", nargs="+")
parser.add_argument("--no-string", action="store_true")
parser.add_argument("--no-header-changes", action="store_true")

args = parser.parse_args()

SYMBOLS_OK = ['~','H','T','.','-']
SYMBOLS_DEL = ['L','M','P','O','S','u','v']
VALID_INS = ('!roll!', '!fermata!', '!trill!')
TRANSLATION_INS = {'roll':'~', 'fermata':'H', 'trill':'T'}
COMPAS_2CHAR = ('||', '::', ':|', '|:' )
NOTE_START = '=_^ABCDEFGabcdefgz'
NOTE_PREFIX = '=_^'
NOTE_BODY = 'ABCDEFGabcdefgz'
NOTE_SUFFIX = ",'"

def extract_note(word):
    note = ''
    mul = ''
    more = ''

    # Get note
    if word[0:1] in NOTE_PREFIX:
        note += word[0:1]
        word = word[1:]
    if word[0:1] in NOTE_BODY:
        note += word[0:1]
        word = word[1:]
    if word[0:1] in NOTE_SUFFIX:
        note += word[0:1]
        word = word[1:]

    # Get multiplier
    while word[0:1] == '/' or word[0:1].isdecimal():
        mul += word[0:1]
        word = word[1:]
    more = word
    return note,mul,more



def process_line(line):

    while line[0:1] == ' ':
        line = line[1:]
    
    # Base case
    if line == '':
        return []

    words = []


    # Check symbols
    if line[0] in SYMBOLS_DEL:
        line = line[1:]
    elif line[0] in SYMBOLS_OK:
        words.append(line[0])
        line = line[1:]
    elif line.startswith(VALID_INS):
        parts = line.split('!')             # ['', symbol, more...]
        symbol = TRANSLATION_INS[''.join(parts[1:2])]
        words.append(symbol)
        line = '!'.join(parts[2:])
    elif line[0] == '!':                    # Other !instructions! invalid
        parts = line.split('!')             # ['', symbol, more...]
        line = '!'.join(parts[2:])
    # Check strings
    elif line[0] == '"':
        parts = line.split('"')             # ['', string, more...]
        if not args.no_string:              # (depends on flag)
            words.append('"' + ''.join(parts[1:2]) + '"')
        line = '"'.join(parts[2:])
    # Check compas changes (2-char): || or :| or |: or ::
    elif line.startswith(COMPAS_2CHAR):
        words.append(line[0:2])
        line = line[2:]
        # Check number: :|1 :|2 ...
        if line[0:1].isdecimal():
            line = line[1:]
    # Check compas change (1-char)
    elif line[0] == '|':
        words.append(line[0])
        line = line[1:]
        # Check number: |1 |2...
        if line[0:1].isdecimal():
            line = line[1:]
    # Check chors or header changes [M:2/4] or [1 [2 ...
    elif line[0] == '[':
        if line[1:2].isdecimal():           # [1 [2 ... (delete)
            line = line[2:]
            if line[0:1] == ',' and line[1:2].isdecimal():  # Case: [1,2 ..
                line = line[2:]
        elif line[2:3] == ':':              # [?:...] (depends on flag)
            parts = line.split(']')         # '[?:???' , more...
            if not args.no_header_changes:
                words.append(parts[0]+"]")
            line = ']'.join(parts[1:])
        elif line[1:2] in NOTE_START or line[1:2] == '':    # Chord
            words.append(line[0])
            line = line[1:]
        else:
            print("ERROR: Unrecognized word ",line)
            exit(1)
    elif line[0] == ']':
        words.append(line[0])
        line = line[1:]
    # Check \
    elif line[0] == '\\':
        line = line[1:]
    # Check comments
    elif line[0] == "%":
        line = ''
    # Check (n: (2 (3 ...
    elif line[0] == '(' and line[1:2].isdecimal():
        words.append(line[0:2])
        line = line[2:]
    # Check slurs ( )   (delete)
    elif line[0] == '(' or line[0] == ')':
        line = line[1:]
    # Check grace notes
    elif line[0] == '{' or line[0] == '}':
        words.append(line[0])
        line = line[1:]
    # Check notes
    elif line[0] in NOTE_START:
        note, mul, more = extract_note(line)
        words.append(note)
        words.append(mul)
        line = more 

    # Others
    else:
        print("ERROR: Unrecognized word ",line)
        exit(2)

    words += process_line(line)

    return words

for f in args.FILE:
    outputlines = []
    with open(f, 'r') as originalfile:
        lines = originalfile.read().split('\n')

    for line in lines:
        # Skip empty lines
        if line == '':
            continue

        # Skip header fields
        elif line[0].isalpha() and line[1] == ":":
            outputlines.append(line)

        # Process line
        else:
            processed_line = process_line(line)
            processed_line = ' '.join(processed_line)
            outputlines.append(processed_line)

    with open("fixed-symbols_"+str(f), 'w') as output:
        output.write('\n'.join(outputlines)+'\n')


