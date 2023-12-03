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
db.execute("CREATE TABLE gear_ratio_candidates AS select nbr.line_number, \
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
AND nbr.end_position + 1 >= sbl.start_position")

# Do a checksum in the previous query
cur = db.execute("SELECT sum(part_number) from gear_ratio_candidates")
query_result = cur.fetchall()
print(query_result)
# Expected result: 554003
# Actual result:   554003

# Delete anything that is not a gear
db.execute("DELETE FROM gear_ratio_candidates \
WHERE symbol != '*'")
db.commit()

# Check how many gears each part number is attached to
db.execute("DROP TABLE IF EXISTS part_number_gear_count")
db.execute("CREATE TABLE part_number_gear_count AS select part_number, \
                                                          line_number, \
                                                          start_position, \
                                                          count(*) as count_gears \
FROM gear_ratio_candidates \
GROUP BY part_number, line_number, start_position \
ORDER BY count_gears, line_number, start_position")



# Count part numbers connected to the gear candidates
db.execute("DROP TABLE IF EXISTS gears")
db.execute("CREATE TABLE gears AS select symbol_line_number, \
                                         symbol_start_position, \
                                         symbol_end_position, \
                                         symbol, \
                                         min(part_number) as part_number_1, \
                                         max(part_number) as part_number_2, \
                                         min(part_number) * max(part_number) as gear_ratio, \
                                         count(*) as part_count \
FROM gear_ratio_candidates \
GROUP BY symbol_line_number, symbol_start_position, symbol_end_position, symbol")

# Get rid of non-gears, ie. the gear candidates not connected to exactly 2 part numbers
db.execute("DELETE FROM gears WHERE part_count != 2")
db.commit()

# Find gear ratios
db.execute("DROP TABLE IF EXISTS gear_ratios")
db.execute("CREATE TABLE gear_ratios AS select l.part_number as left_part_number, \
                                               r.part_number as right_part_number, \
                                               s.symbol_line_number, \
                                               s.symbol_start_position, \
                                               s.symbol_end_position, \
                                               s.symbol, \
                                               s.part_count, \
                                               l.part_number * r.part_number as gear_ratio \
FROM gear_ratio_candidates as l \
INNER JOIN gears as s \
ON l.symbol_line_number = s.symbol_line_number \
AND l.symbol_start_position = s.symbol_start_position \
AND l.symbol = s.symbol \
INNER JOIN gear_ratio_candidates as r \
ON r.symbol_line_number = s.symbol_line_number \
AND r.symbol_start_position = s.symbol_start_position \
AND r.symbol = s.symbol \
AND (l.line_number < r.line_number or l.line_number = r.line_number and l.start_position < r.start_position) \
ORDER BY s.symbol_line_number, s.symbol_start_position, left_part_number, right_part_number")

cur = db.execute("SELECT sum(gear_ratio) from gear_ratios")
query_result = cur.fetchall()
print(query_result)
# Result: 87263515


# Cleanup
if db:
    #db.execute("DROP TABLE IF EXISTS symbols")
    #db.execute("DROP TABLE IF EXISTS numbers")
    #db.execute("DROP TABLE IF EXISTS part_numbers")
    db.close()

