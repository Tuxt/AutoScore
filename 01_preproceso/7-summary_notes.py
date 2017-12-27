
import argparse

parser = argparse.ArgumentParser(description="Show summary of preprocessed ABC code")
parser.add_argument("FILE", help="File to process")
parser.add_argument("-f","--format", help="Type format", type=int, default=0)

args = parser.parse_args()

dic = {}

with open(args.FILE) as f:
    for line in f.read().splitlines():
        for word in line.split():
            if args.format == 1 and "[" in word:
                continue
            if args.format == 2 and ("[" in word or "(" in word):
                continue
                
            dic[word] = dic.get(word,0) + 1

col_width = max(len(word) for word in dic.keys()) + 2

for word,value in dic.items():
    print(word.ljust(col_width) + str(value))

print("TOTAL NOTES:\t" + str(len(dic)))
print("TOTAL CASES:\t" + str(sum(dic.values())))
