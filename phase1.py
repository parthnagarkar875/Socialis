import sqlite3

conn1 = sqlite3.connect('sample.db')
print("Opened the database successfully")

conn = conn1.cursor()


# conn.execute('''CREATE TABLE SAMPLE
#             (ID INT PRIMARY KEY NOT NULL,
#              NAME TEXT NOT NULL
#             );''')

# conn.execute("INSERT INTO SAMPLE (ID,NAME) \
#       VALUES (2, 'Parth')")

# conn1.commit()
output=conn.execute("SELECT COUNT(*) FROM SAMPLE")

# conn.execute("DELETE from SAMPLE where ID = 2")
# conn.execute("DELETE from SAMPLE where ID = 1")

result=output.fetchall()
print(result)

# for row in output:
#     print("ID:", row[0])
#     print("Name:", row[1])
    

# conn.commit()
conn.close()