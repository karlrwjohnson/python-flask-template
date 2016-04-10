import psycopg2

DATABASE='karl'
USER='karl'
HOST='localhost'

# Network database
#dbconn = psycopg2.connect(database=DATABASE, user=USER, hostname=HOST, port=5432)
# Local machine (unix socket)
dbconn = psycopg2.connect(database=DATABASE, user=USER, port=5433)

cursor = dbconn.cursor()

cursor.execute("select id, data from widgets")
for record in cursor:
  print record

