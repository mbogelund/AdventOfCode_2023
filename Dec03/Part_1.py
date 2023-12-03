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

def insert_number(conn, number_tuple):
    """
    Insert number
    :param conn:
    :param number:
    :return: row id
    """
    sql = ''' INSERT INTO numbers(line_number, number, start_position, end_position)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, number_tuple)
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
        position = position + len(symbol)
        #print(symbol_data)
        row_id = insert_symbol(db, symbol_data)
    position = 0
    for number in numbers:
        position = line.find(number, position)
        number_data = (line_number, number, position, position + len(number) - 1)
        position = position + len(number)
        #print(number_data)
        row_id = insert_number(db, number_data)
    #print(line_number)
    line_number += 1
    #print(line)


db.execute("DROP TABLE IF EXISTS part_numbers")
db.execute("CREATE TABLE part_numbers AS select distinct nbr.line_number, \
                                                         sbl.line_number as symbol_line_number, \
                                                         nbr.number as part_number, \
                                                         sbl.symbol \
FROM numbers AS nbr INNER JOIN symbols as sbl ON \
nbr.line_number - 1 <= sbl.line_number AND nbr.line_number + 1 >= sbl.line_number \
AND nbr.start_position - 1 <= sbl.end_position \
AND nbr.end_position + 1 >= sbl.start_position")

cur = db.execute("SELECT sum(part_number) from part_numbers")
query_result = cur.fetchall()
print(query_result)
# Result: 554003

# Cleanup
if db:
    #db.execute("DROP TABLE IF EXISTS symbols")
    #db.execute("DROP TABLE IF EXISTS numbers")
    #db.execute("DROP TABLE IF EXISTS part_numbers")
    db.close()

