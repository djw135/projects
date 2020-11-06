import sqlite3

# Establishing a connection/creating db 
conn = sqlite3.connect('test.db')

# Creating cursor object to interact with the db
cursor = conn.cursor()

# Dropping duplicate table
cursor.execute("DROP TABLE IF EXISTS TEST")

# Creating table
sql = '''CREATE TABLE TEST (
    FIRST_NAME CHAR(20) NOT NULL,
    LAST_NAME CHAR(20),
    AGE INT,
    SEX CHAR(1),
    INCOME FLOAT
)'''

cursor.execute(sql)
print("Table created successfully........")

conn.commit()
conn.close()