
'''
    Translate ABC code to C key
    Delete "anotation"s
    Delete +anotation+s
    Delete repetitions
    Add flat (_), sharp (^) or natural (=) to all notes 
'''

import argparse

parser = argparse.ArgumentParser(description="Translate ABC code to C key")
parser.add_argument("FILE", help="File to process", nargs="+")

args = parser.parse_args()


# INIT STATE FUNCs #
# State for 0 sharps/flats: C (ionian) Am (aeolian)
def initStateC():
    state["C,"] = "="
    state["D,"] = "="
    state["E,"] = "="
    state["F,"] = "="
    state["G,"] = "="
    state["A,"] = "="
    state["B,"] = "="
    state["C"] = "="
    state["D"] = "="
    state["E"] = "="
    state["F"] = "="
    state["G"] = "="
    state["A"] = "="
    state["B"] = "="
    state["c"] = "="
    state["d"] = "="
    state["e"] = "="
    state["f"] = "="
    state["g"] = "="
    state["a"] = "="
    state["b"] = "="
    state["c'"] = "="
    state["d'"] = "="
    state["e'"] = "="
    state["f'"] = "="
    state["g'"] = "="
    state["a'"] = "="
    state["b'"] = "="

# State for 1 sharp: G (ionian) Em (aeolian)
def initStateG():
    state["C,"] = "="
    state["D,"] = "="
    state["E,"] = "="
    state["F,"] = "^"
    state["G,"] = "="
    state["A,"] = "="
    state["B,"] = "="
    state["C"] = "="
    state["D"] = "="
    state["E"] = "="
    state["F"] = "^"
    state["G"] = "="
    state["A"] = "="
    state["B"] = "="
    state["c"] = "="
    state["d"] = "="
    state["e"] = "="
    state["f"] = "^"
    state["g"] = "="
    state["a"] = "="
    state["b"] = "="
    state["c'"] = "="
    state["d'"] = "="
    state["e'"] = "="
    state["f'"] = "^"
    state["g'"] = "="
    state["a'"] = "="
    state["b'"] = "="

# State for 2 sharp: D (ionian) Bm (aeolian)
def initStateD():
    state["C,"] = "^"
    state["D,"] = "="
    state["E,"] = "="
    state["F,"] = "^"
    state["G,"] = "="
    state["A,"] = "="
    state["B,"] = "="
    state["C"] = "^"
    state["D"] = "="
    state["E"] = "="
    state["F"] = "^"
    state["G"] = "="
    state["A"] = "="
    state["B"] = "="
    state["c"] = "^"
    state["d"] = "="
    state["e"] = "="
    state["f"] = "^"
    state["g"] = "="
    state["a"] = "="
    state["b"] = "="
    state["c'"] = "^"
    state["d'"] = "="
    state["e'"] = "="
    state["f'"] = "^"
    state["g'"] = "="
    state["a'"] = "="
    state["b'"] = "="

# State for 3 sharps: A (ionian) F#m (aeolian)
def initStateA():
    state["C,"] = "^"
    state["D,"] = "="
    state["E,"] = "="
    state["F,"] = "^"
    state["G,"] = "^"
    state["A,"] = "="
    state["B,"] = "="
    state["C"] = "^"
    state["D"] = "="
    state["E"] = "="
    state["F"] = "^"
    state["G"] = "^"
    state["A"] = "="
    state["B"] = "="
    state["c"] = "^"
    state["d"] = "="
    state["e"] = "="
    state["f"] = "^"
    state["g"] = "^"
    state["a"] = "="
    state["b"] = "="
    state["c'"] = "^"
    state["d'"] = "="
    state["e'"] = "="
    state["f'"] = "^"
    state["g'"] = "^"
    state["a'"] = "="
    state["b'"] = "="

# State for 4 sharps: E (ionian) C#m (aeolian)
def initStateE():
    state["C,"] = "^"
    state["D,"] = "^"
    state["E,"] = "="
    state["F,"] = "^"
    state["G,"] = "^"
    state["A,"] = "="
    state["B,"] = "="
    state["C"] = "^"
    state["D"] = "^"
    state["E"] = "="
    state["F"] = "^"
    state["G"] = "^"
    state["A"] = "="
    state["B"] = "="
    state["c"] = "^"
    state["d"] = "^"
    state["e"] = "="
    state["f"] = "^"
    state["g"] = "^"
    state["a"] = "="
    state["b"] = "="
    state["c'"] = "^"
    state["d'"] = "^"
    state["e'"] = "="
    state["f'"] = "^"
    state["g'"] = "^"
    state["a'"] = "="
    state["b'"] = "="

# State for 5 sharps: B (ionian) G#m (aeolian)
def initStateB():
    state["C,"] = "^"
    state["D,"] = "^"
    state["E,"] = "="
    state["F,"] = "^"
    state["G,"] = "^"
    state["A,"] = "^"
    state["B,"] = "="
    state["C"] = "^"
    state["D"] = "^"
    state["E"] = "="
    state["F"] = "^"
    state["G"] = "^"
    state["A"] = "^"
    state["B"] = "="
    state["c"] = "^"
    state["d"] = "^"
    state["e"] = "="
    state["f"] = "^"
    state["g"] = "^"
    state["a"] = "^"
    state["b"] = "="
    state["c'"] = "^"
    state["d'"] = "^"
    state["e'"] = "="
    state["f'"] = "^"
    state["g'"] = "^"
    state["a'"] = "^"
    state["b'"] = "="

# State for 1 flat: F (ionian) Dm (aeolian)
def initStateF():
    state["C,"] = "="
    state["D,"] = "="
    state["E,"] = "="
    state["F,"] = "="
    state["G,"] = "="
    state["A,"] = "="
    state["B,"] = "_"
    state["C"] = "="
    state["D"] = "="
    state["E"] = "="
    state["F"] = "="
    state["G"] = "="
    state["A"] = "="
    state["B"] = "_"
    state["c"] = "="
    state["d"] = "="
    state["e"] = "="
    state["f"] = "="
    state["g"] = "="
    state["a"] = "="
    state["b"] = "_"
    state["c'"] = "="
    state["d'"] = "="
    state["e'"] = "="
    state["f'"] = "="
    state["g'"] = "="
    state["a'"] = "="
    state["b'"] = "_"

# State for 2 flats: Bb (ionian) Gm (aeolian)
def initStateBb():
    state["C,"] = "="
    state["D,"] = "="
    state["E,"] = "_"
    state["F,"] = "="
    state["G,"] = "="
    state["A,"] = "="
    state["B,"] = "_"
    state["C"] = "="
    state["D"] = "="
    state["E"] = "_"
    state["F"] = "="
    state["G"] = "="
    state["A"] = "="
    state["B"] = "_"
    state["c"] = "="
    state["d"] = "="
    state["e"] = "_"
    state["f"] = "="
    state["g"] = "="
    state["a"] = "="
    state["b"] = "_"
    state["c'"] = "="
    state["d'"] = "="
    state["e'"] = "_"
    state["f'"] = "="
    state["g'"] = "="
    state["a'"] = "="
    state["b'"] = "_"

# State for 3 flats: Eb (ionian) Cm (aeolian)
def initStateEb():
    state["C,"] = "="
    state["D,"] = "="
    state["E,"] = "_"
    state["F,"] = "="
    state["G,"] = "="
    state["A,"] = "_"
    state["B,"] = "_"
    state["C"] = "="
    state["D"] = "="
    state["E"] = "_"
    state["F"] = "="
    state["G"] = "="
    state["A"] = "_"
    state["B"] = "_"
    state["c"] = "="
    state["d"] = "="
    state["e"] = "_"
    state["f"] = "="
    state["g"] = "="
    state["a"] = "_"
    state["b"] = "_"
    state["c'"] = "="
    state["d'"] = "="
    state["e'"] = "_"
    state["f'"] = "="
    state["g'"] = "="
    state["a'"] = "_"
    state["b'"] = "_"



# EXECUTION #
state = {}

stateFun = {
        "C": initStateC, "Am": initStateC,
        "G": initStateG, "Em": initStateG,
        "D": initStateD, "Bm": initStateD,
        "A": initStateA, "F#m": initStateA,
        "E": initStateE, "C#m": initStateE,
        "B": initStateB, "G#m": initStateB,
        "F": initStateF, "Dm": initStateF,
        "Bb": initStateBb, "Gm": initStateBb,
        "Eb": initStateEb, "Cm": initStateEb
        }

NOTES = "ABCDEFGabcdefg"
OCT = [",","'"]
ALT = ["=", "_", "^"]

for f in args.FILE:
    print("Processing "+f)
    # Read data
    ifile = open(f, 'r')
    data = ifile.readlines()
    ifile.close()

    num_lines = len(data)
    counter = 0

    FLAG_STRING = False     # Flag inside string "anotation"
    FLAG_PLUS = False       # Flag inside plus +anotation+
    FLAG_EXCL = False       # Flag inside excl !anotation!

    with open("Ckey_"+str(f), 'w') as ofile:

        K = ""

        # Process data
        for line in data:
            counter += 1
            print("\r" + str(counter) + "/" + str(num_lines), end="")
            # Empty line
            if len(line) < 2:
                ofile.write(line)
                continue

            # New tune(X)
            if line.startswith("X:"):
                state = {}
                ofile.write(line)
                continue

            # K instruction
            if line.startswith("K:"):
                K = line[2:-1]
                ofile.write("K:C\n")        # New K instruction
                stateFun[K]()               # Init state for K
                continue
            
            # Comments
            if line.startswith("%"):
                continue

            # Other header instructions
            if line[0].isalpha() and line[1] == ":":
                ofile.write(line)
                continue
            # Notes line
            else:
                new_line = ""
                i = 0
                line_len = len(line)
                while i < line_len:
                    current = line[i]
                    # Check string anotations
                    if FLAG_STRING and current != '"':
                        new_line += current
                        i += 1
                        continue
                    if current == '"':
                        new_line += current
                        FLAG_STRING = not FLAG_STRING
                        i += 1
                        continue

                    # Check plus anontations (delete)
                    if FLAG_PLUS and current != '+':
                        i += 1
                        continue
                    if current == '+':
                        FLAG_PLUS = not FLAG_PLUS
                        i += 1
                        continue

                    # Check excl anotations
                    if FLAG_EXCL and current != '!':
                        new_line += current
                        i += 1
                        continue
                    if current == '!':
                        new_line += current
                        FLAG_EXCL = not FLAG_EXCL
                        i += 1
                        continue


                    # Check alteration
                    if current in ALT:
                        # 2-char note
                        if line[i+2:i+3] in OCT and line[i+1:i+2] in NOTES:
                            # Update state
                            note = line[i+1:i+3]
                            state[note] = current
                            # Append and continue
                            new_line += line[i:i+3]
                            i += 3
                            continue
                        # 1-char note
                        elif line[i+1:i+2] in NOTES:
                            # Update state
                            note = line[i+1:i+2]
                            state[note] = current
                            # Append and continue
                            new_line += line[i:i+2]
                            i += 2
                            continue
                    # Check notes without alteration
                    elif current in NOTES:
                        # 2-char note
                        if line[i+1:i+2] in OCT:
                            note = line[i:i+2]
                            i += 2
                        # 1-char note
                        else:
                            note = current
                            i += 1
                        # Append note with state alteration
                        new_line += state[note] + note
                        continue
                    # Check bars
                    elif current == "|":
                        # Reset state
                        stateFun[K]()
                        new_line += current
                        i += 1
                        continue
                    # Bar like :: -> :||:
                    elif current == ":" and line[i+1:i+2] == ":":
                        # Reset state
                        stateFun[K]()
                        new_line += "::"
                        i += 2
                        continue
                    else:
                        new_line += current
                        i += 1

                ofile.write(new_line)
        print("")

