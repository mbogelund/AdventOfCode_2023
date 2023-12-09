# AoC 2023
# Dec08

import re
import sqlite3
from sqlite3 import Error

# Database functions
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn

# Import today's data
data = [l.strip() for l in open("Input/input.txt", "rt")]
#data = [l.strip() for l in open("Input/example.txt", "rt")]
#print(data)


# Part 1

# Create needed database tables
db = create_connection(r"data/pythonsqlite.db")
#db.execute("CREATE TABLE IF NOT EXISTS symbols (line_number NUMBER, symbol TEXT, start_position NUMBER, end_position NUMBER)")
#db.execute("DELETE FROM symbols")
#db.execute("CREATE TABLE IF NOT EXISTS numbers (line_number NUMBER, number STRING, start_position NUMBER, end_position NUMBER)")
#db.execute("DELETE FROM numbers")


lines = []
nodes_dict = {}
node_number = 0
first_key = 'AAA'
for line in data:
    if line:
        if line.find('=') < 0:
            sequence = line
        else:
            node_number = node_number + 1
            key = line.split("=")[0].strip()
            if not first_key:
                first_key = key
            #print(key)
            vertices = (line.split("=")[1].split(",")[0].strip(", ()"), line.split("=")[1].split(",")[1].strip(", ()"))
            #print(vertices)
            nodes_dict[key] = vertices

print(sequence)
#print(nodes_dict)
print(first_key)

step_count = 0
idx = 0
current_key = first_key
while current_key != 'ZZZ' and step_count < 100000:
    step_count = step_count + 1
    current_vertices = nodes_dict[current_key]
    if idx >= len(sequence):
        idx = 0
    if sequence[idx] == 'L':
        tuple_idx = 0
    if sequence[idx] == 'R':
        tuple_idx = 1
    current_key = current_vertices[tuple_idx]
    print(sequence[idx], ' -> ', current_key)
    idx = idx + 1

print(step_count)

# Result: 921
# Evaluation: Too low!

# Result: 18727
# Evaluation: Correct!


# Cleanup
if db:
    #db.execute("DROP TABLE IF EXISTS symbols")
    #db.execute("DROP TABLE IF EXISTS numbers")
    #db.execute("DROP TABLE IF EXISTS part_numbers")
    db.close()

