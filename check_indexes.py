import sqlite3

conn = sqlite3.connect(".optibatch/optibatch.db")
cursor = conn.cursor()

print("Indexes on 'runs':")
cursor.execute("PRAGMA index_list('runs')")
for row in cursor.fetchall():
    print(row)

print("\nIndex info for 'uq_result_hash':")
cursor.execute("PRAGMA index_info('uq_result_hash')")
for row in cursor.fetchall():
    print(row)

conn.close()
