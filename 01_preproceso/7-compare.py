
import argparse

parser = argparse.ArgumentParser(description="Show summary of preprocessed ABC code")
parser.add_argument("FILE", help="File to process")

args = parser.parse_args()

dic = {}

with open(args.FILE) as f:
    for line in f.read().splitlines():
        for word in line.split():
            dic[word] = dic.get(word,0) + 1

total_words = len(dic)
total_occurs = sum(dic.values())

for word,value in dic.items():
    print(word.ljust(20) +
            str(str(value)+"/"+str(total_occurs)).rjust(15) +
            str(" "*5 + str(100*value/total_occurs)+" %").ljust(20).rjust(20) )

print("DICCIONARIO:".ljust(20) + str(total_words) + " pals")
print("OCURRENCIAS:".ljust(20) + str(total_occurs) + " muestras")
