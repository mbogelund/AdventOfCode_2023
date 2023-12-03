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

def insert_symbol(conn, symbol_tuple):
    """
    Insert symbol
    :param conn:
    :param symbol:
    :return: row id
    """
    sql = ''' INSERT INTO symbols(line_number, symbol, start_position, end_position)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, symbol_tuple)
    conn.commit()
    return cur.lastrowid


# Import today's data
data = [l.strip() for l in open("Input/input.txt", "rt")]
#print(data)


# Part 1

# Create needed database tables
db = create_connection(r"data/pythonsqlite.db")
db.execute("CREATE TABLE IF NOT EXISTS symbols (line_number NUMBER, symbol TEXT, start_position NUMBER, end_position NUMBER)")
db.execute("DELETE FROM symbols")
db.execute("CREATE TABLE IF NOT EXISTS numbers (line_number NUMBER, number STRING, start_position NUMBER, end_position NUMBER)")
db.execute("DELETE FROM numbers")


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
        row_id = insert_symbol(db, symbol_data)
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



# Cleanup
if db:
    db.close()

