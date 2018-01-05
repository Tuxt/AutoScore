
'''
    Translate ABC code to default length 1/8
'''

from fractions import Fraction
import argparse

parser = argparse.ArgumentParser(description="Translate ABC code from L:1/8 and L:1/4 to L:1/8")
parser.add_argument("FILE", help="File to process", nargs="+")

args = parser.parse_args()

NOTES = "ABCDEFGabcdefg"    # Note chars
VALID = ",'123456789/"      # Valid chars appended to notes

for f in args.FILE:
    # Read data
    ifile = open(f,'r')
    data = ifile.readlines()
    ifile.close()
    with open("len1-8_"+str(f), 'w') as ofile:
        
        # Process data
        L = "1/8"
        for line in data:
            # Empty line
            if len(line) < 2:
                ofile.write(line)
                continue

            # New tune (X)
            if line.startswith("X:"):
                L = "1/8"                       # Reset L
                # Read until L: instruction or new tune
                ofile.write(line)
                continue
            
            # L instruction
            if line.startswith("L:"):
                L = line[2:-1]
                ofile.write("L:1/8\n")          # New L instruction
                continue

            # Other header instructions
            if line[0].isalpha() and line[1] == ":":
                ofile.write(line)
                continue
            # Notes
            elif L == "1/8":                    # OK
                ofile.write(line)
                continue
            elif L == "1/4":                    # Update notes
                new_line = ""                   # Updated line var
                i = 0
                line_len = len(line)
                STR_FLAG = False                # Flag: string opened
                while i < line_len:
                    current = line[i]
                    if current in NOTES and not STR_FLAG:
                        note = current
                        i += 1
                        current = line[i]
                        while current in VALID:
                            note += current
                            i += 1
                            current = line[i]
                        print("PROCESSING 1/4 note: "+note)
                        # Get multiplier
                        # Notes without multiplier
                        if (len(note) == 1) or (len(note) == 2 and note[1] in ["'",","]):
                            new_line += note
                            mul = '1'
                        elif note[1] in ["'",","]:
                            new_line += note[:2]    # Append note
                            mul = note[2:]          # Get multiplier
                        else:
                            new_line += note[:1]    # Append note
                            mul = note[1:]          # Get multiplier
                        # Fix multiplier
                        if mul.startswith("/"):
                            mul = '1' + mul
                        if mul.endswith("/"):
                            mul += '2'
                        print("\tDetected multiplier: "+mul)
                        # Update multiplier
                        frac = Fraction(mul)
                        frac = frac * 2
                        print("\tNew Multiplier: "+str(frac))
                        # Append multiplier if need
                        if str(frac) != '1':
                            if frac.numerator == 1:
                                new_line += str(frac)[1:]
                            else:
                                new_line += str(frac)       # Append updated multiplier
                    else:
                        if current == '"':
                            STR_FLAG = not STR_FLAG
                        new_line += current
                        i += 1
                        continue
                ofile.write(new_line)

