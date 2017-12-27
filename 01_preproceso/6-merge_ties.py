
'''
    Merge ties: =D2 - =D/2 => =D5/2
    TODO...
'''

import argparse

parser = argparse.ArgumentParser(description="Recode ABC code deleting (n and splitting multipliers from notes")
parser.add_argument("FILE", help="File to process")
parser.add_argument("-o", "--output", help="Output file", default="output.abc")

args = parser.parse_args()




odata = []

with open(args.FILE) as ifile:
    idata = ifile.read().splitlines()
    for iline in idata:
        oline = []
        for iword in iline.split():
            # Delete (n
            if iword.startswith("("):
                continue
            
            # Split note-multiplier if flag is True
            if not args.split:
                oline.append(iword)
                continue
            if iword.startswith("_") or iword.startswith("^") or iword.startswith("="):
                # 2-char notes
                if iword[2:3] in [",","'"]:
                    oline.append(iword[0:3])
                    oline.append(iword[3:])
                # 1-char notes
                else:
                    oline.append(iword[0:2])
                    oline.append(iword[2:])
            # Append other words
            else:
                oline.append(iword)
        
        # Join new words and append to odata
        odata.append(" ".join(oline))
    
    # Join lines from odata
    result_data = "\n".join(odata)+"\n"

with open(args.output,'w') as ofile:
    ofile.write(result_data)


