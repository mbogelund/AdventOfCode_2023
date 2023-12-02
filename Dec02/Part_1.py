import re

data = [l.strip() for l in open("Input/input.txt", "rt")]

ids = [re.split("\s",re.split(":", l.strip(), 1)[0])[1] for l in open("Input/input.txt", "rt")]
#re.split("\s",re.split(":", txt, 1)[0])[1]

split_data1 = [re.split(":", l.strip(), 1) for l in open("Input/input.txt", "rt")]
split_data2 = [[{"ID": int(re.split("\s", l[0], 1)[1])}, re.split(";", l[1])] for l in split_data1]

split_data = []
for game in split_data2:
    round_list = []
    for round in game[1]:
        #print(round)
        round_list.append(re.split(",", round))
        #print(draw_list)
    split_data.append([game[0], round_list])
print(split_data[99])

