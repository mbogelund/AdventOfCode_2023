# AoC 2023
# Dec11

from math import exp
import re
import sqlite3
from sqlite3 import Error
from telnetlib import GA

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

def insert_input_line(conn, input_line_tuple):
    """
    Insert input_line
    :param conn:
    :param input_line_tuple:
    :return: row id
    """
    sql = ''' INSERT INTO INPUT(line_number, input)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, input_line_tuple)
    conn.commit()
    return cur.lastrowid


# Import today's data
#data = [l.strip() for l in open("Input/example.txt", "rt")]
data = [l.strip() for l in open("Input/input.txt", "rt")]
#print(data)


# Part 2

# Create needed database tables
db = create_connection(r"data/pythonsqlite.db")
db.execute("CREATE TABLE IF NOT EXISTS INPUT (line_number NUMBER, input TEXT)")
db.execute("DELETE FROM INPUT")
#db.execute("DROP TABLE IF EXISTS NEW_SEQUENCES")
#db.execute("CREATE TABLE IF NOT EXISTS NEW_SEQUENCES (line_number NUMBER, new_sequence, extrapolated_value)")
#db.execute("DELETE FROM NEW_SEQUENCES")
#db.execute("CREATE TABLE IF NOT EXISTS SEQUENCES (line_number NUMBER, number STRING, start_position NUMBER, end_position NUMBER)")
#db.execute("DELETE FROM SEQUENCES")

# Read input data into table
lines = []
line_number = 0
for line in data:
    line_number += 1
    if line:
        row_id = insert_input_line(db, (line_number, line))
        lines.append(line)

galaxy_columns = [0 for idx in range(len(lines[0]))]
galaxy_rows = [0 for idx in range(len(lines))]

print()
print("Galaxy columns:")    
print(galaxy_columns)
print()
print("Galaxy rows:")
print(galaxy_rows)

row_idx = -1
for line in lines:
    row_idx = row_idx + 1
    galaxy_idx = line.find("#")
    if galaxy_idx >= 0:
        galaxy_rows[row_idx] = 1
        while galaxy_idx >= 0:
            galaxy_columns[galaxy_idx] = galaxy_columns[galaxy_idx] + 1
            galaxy_idx = line.find("#", galaxy_idx + 1)

print()
print("Galaxy columns:")    
print(galaxy_columns)
print()
print("Galaxy rows:")
print(galaxy_rows)
    
#print("Original universe:")
#for line in lines:
#    print(line)

# Make a dictionay of galaxy coordinates
galaxy_dict = {}
galaxy_number = 0
for row_idx in range(len(lines)):
    #print(lines[row_idx])
    for column_idx in range(len(lines[row_idx])):
        if lines[row_idx][column_idx] == '#':
            galaxy_number = galaxy_number + 1
            galaxy_dict[galaxy_number] = (row_idx, column_idx)
            
print()
print("Galaxy dictionary:")
print(galaxy_dict)

voidness_multiplyer = 1000000
voidness_column_indices = [idx for idx, element in enumerate(galaxy_columns) if element == 0]
voidness_row_indices = [idx for idx, element in enumerate(galaxy_rows) if element == 0]

print()
print(voidness_column_indices)
print()
print(voidness_row_indices)

galaxy_distances = {}
for from_galaxy in range(1, galaxy_number):
    for to_galaxy in range(from_galaxy + 1, galaxy_number + 1):
        edge = (from_galaxy, to_galaxy)
        from_coordinate = galaxy_dict[from_galaxy]
        to_coordinate = galaxy_dict[to_galaxy]
        voidness_counter = 0
        for void_space in voidness_row_indices:
            if min(from_coordinate[0], to_coordinate[0]) < void_space and max(from_coordinate[0], to_coordinate[0]) > void_space:
                voidness_counter = voidness_counter + 1
        for void_space in voidness_column_indices:
            if min(from_coordinate[1], to_coordinate[1]) < void_space and max(from_coordinate[1], to_coordinate[1]) > void_space:
                voidness_counter = voidness_counter + 1
        galaxy_distance = abs(from_coordinate[0] - to_coordinate[0]) + abs(from_coordinate[1] - to_coordinate[1]) + voidness_counter * (voidness_multiplyer - 1)
        galaxy_distances[edge] = galaxy_distance
        #print()
        #print(edge)
        #print(voidness_counter)
        #print(galaxy_distance)

print()
print("Galaxy distances:")
print(galaxy_distances)

part_2_answer = sum(galaxy_distances.values())
print(part_2_answer)

# Result: 9605127
# Evaluation: Correct!


# Part 2

# Result: 
# Evaluation: 



# Cleanup
if db:
    #db.execute("DROP TABLE IF EXISTS INPUT")
    #db.execute("DROP TABLE IF EXISTS SEQUENCES")
    #db.execute("DROP TABLE IF EXISTS NEW_SEQUENCES")
    db.close()

