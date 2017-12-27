
'''
    Simplifies redundant representations of notes
        _D -> ^C
'''

import sys
import argparse

parser = argparse.ArgumentParser(description="Simplifies redundant repsentations of notes\n")
parser.add_argument("FILE", help="File to process")
parser.add_argument("-o", "--output", help="Output file", default="output.abc")

args = parser.parse_args()

# Translation from flat
flat = {  "D,": "^C,",
          "E,": "^D,",
          "F,": "=E,",
          "G,": "^F,",
          "A,": "^G,",
          "B,": "^A,",
          "C" : "=B,",
          "D" : "^C" ,
          "E" : "^D" ,
          "F" : "=E" ,
          "G" : "^F" ,
          "A" : "^G" ,
          "B" : "^A" ,
          "c" : "=B" ,
          "d" : "^c" ,
          "e" : "^d" ,
          "f" : "=e" ,
          "g" : "^f" ,
          "a" : "^g" ,
          "b" : "^a" ,
          "c'": "=b" ,
          "d'": "^c'",
          "e'": "^d'",
          "f'": "=e'",
          "g'": "^f'",
          "a'": "^g'",
          "b'": "^a'"
        }

def transformSingleNote(note):
    # Flats
    if "_" in note:
        parts = note.split("_")
        new_note = parts[0]
        if parts[1][1:2] in ["'", ","]:
            new_note += flat[parts[1][:2]]
            new_note += parts[1][2:]
        else:
            new_note += flat[parts[1][:1]]
            new_note += parts[1][1:]
        return new_note
        
    # Sharps
    elif "^" in note:
        # #E -> F
        if "e" in note.lower():
            parts = note.split("^")
            new_note = parts[0]
            if parts[1][1:2] == "'":    # ^e' -> =f'
                new_note += "=f'"
                new_note += parts[1][2:]
            elif parts[1][1:2] == ",":  # ^E, -> =F,
                new_note += "=F,"
                new_note += parts[1][2:]
            elif parts[1][0] == "e":    # ^e  -> =f
                new_note += "=f"
                new_note += parts[1][1:]
            else:                       # ^E  -> =F
                new_note += "=F"
                new_note += parts[1][1:]
            return new_note
        # #B -> C
        elif "b" in note.lower():
            parts = note.split("^")
            new_note = parts[0]
            if parts[1][1:2] == "'":    # ^b' -> ^b' (no next)
                new_note = note
            elif parts[1][1:2] == ",":  # ^B, -> =C
                new_note += "=C"
                new_note += parts[1][2:]
            elif parts[1][0] == "b":    # ^b  -> =c'
                new_note += "=c'"
                new_note += parts[1][1:]
            else:                       # ^B  -> =c
                new_note += "=c"
                new_note += parts[1][1:]
            return new_note
        # Others
        else:
            return note

    # Natural
    else:
        return note

'''
    Transform words with chords and (n
'''
def transformMultiples(word):
    result = []
    
    # (n + chord
    if ("[" in word) and ("(" in word):
        # Check ~ and [(n notes]
        if "~" in word:
            print("Error: Invalid ~ in chord: " + word, file=sys.stderr)
            exit(1)
        if word.index("[") < word.index("("):
            print("Error: Invalid (n in chord: "+word, file=sys.stderr)
            exit(2)

        chord_index = word.index("[")
        result.append(word[:chord_index])
        chord_result = transformMultiples(word[chord_index:])
        result += chord_result
        return result

    # Chord
    elif ("[" in word):
        # Check ~
        if "~" in word:
            print("Error: Invalid ~ in chord: " + word, file=sys.stderr)
            exit(1)

        # Split notes
        notes = word[1:-1]
        for i in range(len(notes)-1, -1, -1):
            if notes[i] in ["^", "_", "="]:
                result.append(notes[i:])
                notes = notes[:i]

        # Transform notes
        for i in range(len(result)):
            result[i] = transformSingleNote(result[i])

        # Add chord symbol
        result.append("[" + str(len(result)))
        result.reverse()
        return result
    
    # (n
    elif "(" in word:
        prefix = "("
        for i in range(1, len(word)):
            if word[i].isdecimal():
                prefix += word[i]
            else:
                break
        note = transformSingleNote(word[i:])
        return [prefix, note]


# Read data
with open(args.FILE) as ifile:
    idata = ifile.read().splitlines()

odata = []

for iline in idata:
    iwords = iline.split()
    owords = []
    for word in iwords:

        # (n
        # Chords:   [~^e'2=E2/3_D,/2] -> [3 ~=f'2 =E2/3 _D,/2
        if "(" in word or "[" in word:
            print(word + "\t->\t" + str(transformMultiples(word)))
            # Chord symbol
            owords += transformMultiples(word)
            
        # Single note
        else:
            note = transformSingleNote(word)
            owords.append(note)

    oline = " ".join(owords)
    odata.append(oline)

# Write data
with open(args.output, 'w') as ofile:
    ofile.write("\n".join(odata) + "\n")
