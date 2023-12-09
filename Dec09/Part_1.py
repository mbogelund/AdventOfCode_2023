# AoC 2023
# Dec09

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

def insert_new_sequence(conn, new_sequence_tuple):
    """
    Insert new sequence
    :param conn:
    :param new_sequence_tuple:
    :return: row id
    """
    sql = ''' INSERT INTO NEW_SEQUENCES(line_number, new_sequence, extrapolated_value)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, new_sequence_tuple)
    conn.commit()
    return cur.lastrowid


def get_next_number(sequence):
    # Base case: All zeroes
    if not re.sub('[0,\s]', '', sequence):
        next_char = " 0"
    else:
        sequence_list = [int(item) for item in sequence.split()]
        increments_list = [sequence_list[idx] - sequence_list[idx-1] for idx in range(1, len(sequence_list))]
        increments_sequence = ' '.join([str(item) for item in increments_list])
        #print(sequence_list)
        #print(increments_list)
        #print(increments_sequence)

        extended_incements_sequence = get_next_number(increments_sequence)
        extended_incements_sequence_list = [int(item) for item in extended_incements_sequence.split()]

        next_char = " " + str(sequence_list[-1] + extended_incements_sequence_list[-1])
    return sequence + next_char

def get_part_1_answer(conn):
    cur = db.execute("SELECT sum(extrapolated_value) from NEW_SEQUENCES")
    query_result = cur.fetchall()
    return query_result

# Import today's data
#data = [l.strip() for l in open("Input/example.txt", "rt")]
data = [l.strip() for l in open("Input/input.txt", "rt")]
#print(data)


# Part 1

# Create needed database tables
db = create_connection(r"data/pythonsqlite.db")
db.execute("CREATE TABLE IF NOT EXISTS INPUT (line_number NUMBER, input TEXT)")
db.execute("DELETE FROM INPUT")
#db.execute("DROP TABLE IF EXISTS NEW_SEQUENCES")
db.execute("CREATE TABLE IF NOT EXISTS NEW_SEQUENCES (line_number NUMBER, new_sequence, extrapolated_value)")
db.execute("DELETE FROM NEW_SEQUENCES")


db.execute("CREATE TABLE IF NOT EXISTS SEQUENCES (line_number NUMBER, number STRING, start_position NUMBER, end_position NUMBER)")
db.execute("DELETE FROM SEQUENCES")

# Read input data into table
lines = []
line_number = 0
for line in data:
    line_number += 1
    if line:
        row_id = insert_input_line(db, (line_number, line))
        new_sequence = get_next_number(line)
        #print(line, ' ---> ', new_sequence)
        row_id = insert_new_sequence(db, (line_number, new_sequence, [int(item) for item in new_sequence.split()][-1]))

part_1_answer = get_part_1_answer(db)
print(part_1_answer)

# Result: 1974913025
# Evaluation: Correct!

# Cleanup
if db:
    #db.execute("DROP TABLE IF EXISTS INPUT")
    #db.execute("DROP TABLE IF EXISTS SEQUENCES")
    #db.execute("DROP TABLE IF EXISTS NEW_SEQUENCES")
    db.close()

