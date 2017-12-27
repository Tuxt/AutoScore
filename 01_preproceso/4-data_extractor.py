
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

ALT = ["=", "^", "_"]
OCT = [",", "'"]
NOTES = "abcdefgABCDEFG"

ofile = open(args.output, 'w')

for f in args.FILE:
    print("Processing: " + f)
    ifile = open(f, 'r')
    data = ifile.readlines()
    ifile.close()

    data_line = ""
    for line in data:

        # Skip empty lines
        if line == "\n":
            continue
        
        # Skip comments
        #if line[0] "%":
        #    continue
        
        # Check new tune header (reset data_line: 1 tune / line)
        if line.startswith("X:"):
            #print("\tTUNE: "+line[2:-1])
            if data_line != "":
                data_line += "\n"
                ofile.write(data_line)
                data_line = ""
            continue

        # Skip header lines
        if line[0].isalpha() and line[1] == ":":
            continue
        
        # Set vars
        FLAG_CHORD = False  # Inside chord
        state = 0           # 0 = No | 1 = "(n" | 2 = "~" | 3 = "^|_|=" | 4 = pitch | 5 = mul | 6 = "-"
        i = 0               # Index
        line_len = len(line)

        # Analize notes
        while i < line_len:
            current = line[i]
            nextVal = line[i+1:i+2]

            # Skip spaces
            if current == " ":
                i += 1
                continue

            # Skip invalid before notes
            if state == 0 and not (current in ["(", "[", "~", "^", "_", "="]):
                i += 1
                continue
            
            # Skip fields within the body
            if state == 0 and current == "[" and line[i+2:i+3] == ":":
                i += 1
                continue

            # Check for "(n": From state 0 to 1 only
            if state < 1:
                if current == "(" and nextVal.isdecimal():
                    state = 1
                    data_line += current+nextVal
                    i += 2
                    continue
                # Skip slur
                elif current == "(":
                    i += 1
                    continue
                
            
            # Check for "[" (open chord) (Skip [1 [2 [3...)
            if state < 2 and current == "[" and not FLAG_CHORD and not nextVal.isdecimal():
                FLAG_CHORD = True
                data_line += current
                i += 1
                continue
            elif state < 2 and current == "[" and nextVal.isdecimal():
                i += 2
                continue

            # Check for "~" (tilde)
            if state < 2 and current == "~":
                state = 2
                data_line += current
                i += 1
                continue

            # Check for alterations (=, ^, _)
            if state < 3 and current in ALT:
                state = 3
                data_line += current
                i += 1
                continue

            # Check for pitch
            if state == 3:
                # 2-char note
                if current in NOTES and nextVal in OCT:
                    state = 4
                    data_line += current+nextVal
                    i += 2
                    continue
                # 1-char note
                elif current in NOTES:
                    state = 4
                    data_line += current
                    i += 1
                    continue
                else:
                    print("Error: Expected note on pos " + str(i) + "\n\t" + line, file=sys.stderr)
                    #i += 1
                    #continue
                    exit(1)

            # Check for multiplier
            if state == 4:
                mul = ""
                mulIndex = i
                while line[mulIndex] in "123456789/":
                    mul += line[mulIndex]
                    mulIndex += 1
                i = mulIndex
                state = 5
                data_line += mul
                continue

            # Check for tie "-"
            if (state == 4 or state == 5) and current == "-":
                state = 6
                data_line += current
                i += 1
                continue

            # Check for "]" (close chord) or final note
            if (state == 4 or state == 5 or state == 6):
                # Opened. Current close
                if FLAG_CHORD and current == "]":
                    FLAG_CHORD = False
                    data_line += current+" "
                    i += 1
                    state = 0
                    continue
                # Opened. More notes
                elif FLAG_CHORD:
                    state = 0           # No read char, restart state
                    continue
                # End of note (no chord)
                else:
                    data_line += " "    # Append space (new note, new word)
                    state = 0           # Restart state for new note
                    continue

            # (State, char) not valid
            print("Error: Invalid (state,char) = (" + str(state) + "," + str(current) + ")\n" + \
                    "\tFile: " + str(f) + " Pos: " + str(i) + "\n" + \
                    "\tLINE: " + line, file=sys.stderr)
            exit(2)


    data_line += "\n"
    ofile.write(data_line)
ofile.close()
exit(0)
            

                
