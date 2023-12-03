import re

import db_tools

# Import today's data
data = [l.strip() for l in open("Input/input.txt", "rt")]
#print(data)


# Part 1

# Create needed database tables
db.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, age NUMBER, fav_food STRING)")

lines = []
line_number = 0
for line in data:
    symbols = re.sub('\d', ' ', line).replace('.', ' ').split()
    #print(symbols)
    numbers =  re.sub('\D', ' ', line).replace('.', ' ').split()
    #print(numbers)

    position = 0
    for symbol in symbols:
        position = line.find(symbol, position)
        symbol_data = (line_number, symbol, position, position + len(symbol) - 1)
        position += 1
        print(symbol_data)
    position = 0
    for number in numbers:
        position = line.find(number, position)
        number_data = (line_number, number, position, position + len(number) - 1)
        position += 1
        print(number_data)
    line_number += 1
    #print(line_number)
    print(line)
# Part 2

