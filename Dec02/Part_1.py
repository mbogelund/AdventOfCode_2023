import re

data = [l.strip() for l in open("Input/input.txt", "rt")]

ids = [re.split("\s",re.split(":", l.strip(), 1)[0])[1] for l in open("Input/input.txt", "rt")]
#re.split("\s",re.split(":", txt, 1)[0])[1]

print(ids)

