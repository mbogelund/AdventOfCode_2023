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


# Part 2
db = create_connection(r"data/pythonsqlite.db")
# Find gear candidates - we want gears connected to exactly 2 part numbers
db.execute("DROP TABLE IF EXISTS gear_ratio_candidates")
db.execute("CREATE TABLE gear_ratio_candidates AS select distinct nbr.line_number, \
                                                                  nbr.start_position, \
                                                                  nbr.end_position, \
                                                                  sbl.line_number as symbol_line_number, \
                                                                  sbl.start_position as symbol_start_position, \
                                                                  sbl.end_position as symbol_end_position, \
                                                                  nbr.number as part_number, \
                                                                  sbl.symbol \
FROM numbers AS nbr INNER JOIN symbols as sbl ON \
nbr.line_number - 1 <= sbl.line_number AND nbr.line_number + 1 >= sbl.line_number \
AND nbr.start_position - 1 <= sbl.end_position \
AND nbr.end_position + 1 >= sbl.start_position \
AND sbl.symbol = '*'")

# Count part numbers connected to the gear candidates
db.execute("DROP TABLE IF EXISTS gears")
db.execute("CREATE TABLE gears AS select line_number as symbol_line_number, \
                                                        symbol_start_position, \
                                                        symbol_end_position, \
                                                        symbol, \
                                                        count(*) as part_count \
FROM gear_ratio_candidates \
GROUP BY symbol_line_number, symbol_start_position, symbol_end_position, symbol")

# Get rid of non-gears, ie. the gear candidates not connected to exactly 2 part numbers
db.execute("DELETE FROM gears WHERE part_count <> 2")
db.commit()

#cur = db.execute("SELECT sum(part_number) from part_numbers")
#query_result = cur.fetchall()
#print(query_result)


# Cleanup
if db:
    #db.execute("DROP TABLE IF EXISTS symbols")
    #db.execute("DROP TABLE IF EXISTS numbers")
    #db.execute("DROP TABLE IF EXISTS part_numbers")
    db.close()

