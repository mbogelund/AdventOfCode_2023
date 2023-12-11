# AoC 2023
# Dec10

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

def find_2_connections(node_tuple, lines):
    connections_list = []

    this_char = lines[node_tuple[0]][node_tuple[1]]
    #print(this_char)

    # Connection above
    if node_tuple[0] > 0:
        above = (node_tuple[0] - 1, node_tuple[1])
        above_char = lines[above[0]][above[1]]
        if above_char in ["S", "|", "7", "F"] and this_char in ["S", "|", "J", "L"]:
            connections_list.append((node_tuple[0] - 1, node_tuple[1]))
    # Connection left
    if node_tuple[1] > 0:
        left = (node_tuple[0], node_tuple[1] - 1)
        left_char = lines[left[0]][left[1]]
        if left_char in ["S", "-", "L", "F"] and this_char in ["S", "-", "J", "7"]:
            connections_list.append((node_tuple[0], node_tuple[1] - 1))
    # Connection right
    if node_tuple[1] < len(lines[0]) - 1:
        right = (node_tuple[0], node_tuple[1] + 1)
        right_char = lines[right[0]][right[1]]
        if right_char in ["S", "-", "7", "J"] and this_char in ["S", "-", "F", "L"]:
            connections_list.append((node_tuple[0], node_tuple[1] + 1))
    # Connetion below
    if node_tuple[0] < len(lines) - 1:
        below = (node_tuple[0] + 1, node_tuple[1])
        below_char = lines[below[0]][below[1]]
        if below_char in ["S", "|", "L", "J"] and this_char in ["S", "|", "7", "F"]:
            connections_list.append((node_tuple[0] + 1, node_tuple[1]))
    
    #print(connections_list)
    return connections_list[0], connections_list[1]

# Import today's data
#data = [l.strip() for l in open("Input/example.txt", "rt")]
data = [l.strip() for l in open("Input/example2.txt", "rt")]
#data = [l.strip() for l in open("Input/input.txt", "rt")]
#print(data)


# Part 1

# Create needed database tables
db = create_connection(r"data/pythonsqlite.db")
db.execute("CREATE TABLE IF NOT EXISTS INPUT (line_number NUMBER, input TEXT)")
db.execute("DELETE FROM INPUT")

# Read input data into table
lines = []

distance_rows = []
distance_cells = []

start_char = "S"

line_number = 0
for line in data:
    line_number += 1
    if line:
        row_id = insert_input_line(db, (line_number, line))
        line_list = [cell for cell in line]
        lines.append(line_list)
        
        distance_cells = [0 for cell in line]
        distance_rows.append(distance_cells)

        idx = line.find(start_char)
        if idx >= 0:
            start_row = len(lines) - 1
            start_column = idx
            start_cell = (start_row, start_column)

#print(lines)
rows = len(lines)
columns = len(lines[0])

#print("rows: ", rows)
#print("columns: ", columns)
#print("start_row: ", start_row)
#print("start_column: ", start_column)

#print(distance_rows)

# Every node is identified uniquely by its coordinates (row, column)
# Every node on the loop has exactly 2 connections to other nodes
connections_dict = {}
max_distance = 0

#current_char = lines[connection1[0]][connection1[1]]

#print(current_char)
#print(distance_rows)
#print(connections_dict)

# First, we move one way round...
for direction in range(0, 2):
    # Initilize traversal of loop at start cell "S"
    current_cell = start_cell
    current_distance = 0
    connection1, connection2 = find_2_connections(current_cell, lines)
    connections_dict[str(current_cell[0]) + ',' + str(current_cell[1])] = [connection1, connection2]

    # Take the first step away from S
    previous_cell = start_cell
    if distance_rows[connection1[0]][connection1[1]] == 0 or distance_rows[connection1[0]][connection1[1]] > 1:
        current_cell = connection1
    else:
        current_cell = connection2
    current_char = lines[current_cell[0]][current_cell[1]]
    current_distance = current_distance + 1
    distance_rows[current_cell[0]][current_cell[1]] = current_distance
    
    while current_char != start_char and current_distance < 10000:
        # Register info on current cell
        registered_distance = distance_rows[current_cell[0]][current_cell[1]]
        if registered_distance == 0:
            distance_rows[current_cell[0]][current_cell[1]] = current_distance
        else:
            distance_rows[current_cell[0]][current_cell[1]] = min(current_distance, registered_distance)
            max_distance = max(max_distance, min(current_distance, registered_distance))
        #print(distance_rows)
        connection1, connection2 = find_2_connections(current_cell, lines)
        if (connection1 == start_cell and previous_cell != start_cell) or connection1 != previous_cell:
            next_cell = connection1
        else:
            next_cell = connection2
        connections_dict[str(current_cell[0]) + ',' + str(current_cell[1])] = [connection1, connection2]

        # Move to next cell
        previous_cell = current_cell
        current_cell = next_cell
        current_char = lines[current_cell[0]][current_cell[1]]
        current_distance = current_distance + 1
    
#for distance_line in distance_rows:
#    print(distance_rows)

part_1_answer = max_distance

#part_1_answer = get_part_1_answer(db)
print(part_1_answer)

# Result: 1974913025
# Evaluation: Correct!


# Part 2

# Make a layout map, and mark pipe segments with 1s
layout_map_rows = [row.copy() for row in distance_rows]

for row_idx in range(len(layout_map_rows)):
    for col_idx in range(len(layout_map_rows[row_idx])):
        if layout_map_rows[row_idx][col_idx] > 0 or lines[row_idx][col_idx] == "S":
            layout_map_rows[row_idx][col_idx] = 1
        else:
            layout_map_rows[row_idx][col_idx] = 0


print("line_list:")
for row in lines:
    print(row)
print()
print("distance_rows:")
for row in distance_rows:
    print(row)
print()
print("layout_map_rows:")
for row in layout_map_rows:
    print(row)



# Result: 
# Evaluation: 

# Cleanup
if db:
    #db.execute("DROP TABLE IF EXISTS INPUT")
    #db.execute("DROP TABLE IF EXISTS SEQUENCES")
    #db.execute("DROP TABLE IF EXISTS NEW_SEQUENCES")
    db.close()

