import re

data = [l.strip() for l in open("Input/input.txt", "rt")]

ids = [re.split("\s",re.split(":", l.strip(), 1)[0])[1] for l in open("Input/input.txt", "rt")]
#re.split("\s",re.split(":", txt, 1)[0])[1]

split_data1 = [re.split(":", l.strip(), 1) for l in open("Input/input.txt", "rt")]
split_data2 = [[{"ID": int(re.split("\s", l[0], 1)[1])}, re.split(";", l[1])] for l in split_data1]

split_data3 = []
for game in split_data2:
    round_list = []
    for round in game[1]:
        #print(round)
        round_list.append(re.split(",", round))
        #print(draw_list)
    split_data3.append([game[0], round_list])
#print(split_data3[99])
# [{'ID': 100}, [[' 8 red', ' 2 blue', ' 1 green'], [' 2 blue', ' 4 red', ' 2 green'], [' 9 red', ' 1 green'], [' 2 green', ' 2 red'], [' 3 red', ' 5 blue'], [' 5 blue', ' 8 red']]]

split_data4 = []
for game in split_data3:
    round_list = []
    for round in game[1]:
        draw_dict = {'red': 0, 'green': 0, 'blue': 0}
        for draw in round:
            a, b = draw.strip(' ').split()
            draw_dict[b.strip()] = int(a.strip())
            #print(draw_dict)
        round_list.append(draw_dict)
        #print(round_list)
    split_data4.append([game[0], round_list])
#print(split_data4[99])
[{'ID': 100}, [{'red': 8, 'green': 1, 'blue': 2}, {'red': 4, 'green': 2, 'blue': 2}, {'red': 9, 'green': 1, 'blue': 0}, {'red': 2, 'green': 2, 'blue': 0}, {'red': 3, 'green': 0, 'blue': 5}, {'red': 8, 'green': 0, 'blue': 5}]]

split_data5 = []
for game in split_data4:
    max_dict = {'red': 0, 'green': 0, 'blue': 0}
    for round in game[1]:
        for color in max_dict:
            max_dict[color] = max(round[color], max_dict[color])
    split_data5.append([game[0], max_dict])
#print(split_data5[99])

sum_valid_games = sum(game[0]["ID"] * (game[1]["red"] <= 12) * (game[1]["green"] <= 13) * (game[1]["blue"] <= 14) for game in split_data5)
print("Sum of ID's of possible games: ", sum_valid_games)
