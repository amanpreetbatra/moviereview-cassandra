import json
import multiprocessing as mp
import cassandra
from cassandra.query import BatchStatement


from cassandra.cluster import Cluster

cluster = Cluster()
session = cluster.connect(['127.0.0.1'])

# Create keyspace and table
session.execute("CREATE KEYSPACE IF NOT EXISTS movie_keyspace WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 }")
session.execute("CREATE TABLE IF NOT EXISTS movie_keyspace.reviews (review_id int PRIMARY KEY, data text)")

def insert_batch(batch):
    batch_stmt = BatchStatement()
    for item in batch:
        idd = item.pop("review_id", None)
    # Insert data into Cassandra table
    #     session.execute("INSERT INTO movie_keyspace.reviews (review_id, data) VALUES (%s, %s)", (data['review_id'], data))
        query = '''
                INSERT INTO movie_keyspace.reviews (id, data) VALUES (%s, %s)
                '''
        batch_stmt.add(query, (idd, item['data']))
        session.execute(batch_stmt)


with open('data.json', 'r') as f:
    data = json.load(f)

num_processes = 4

batch_size = len(data) // num_processes
batches = [data[i:i + batch_size] for i in range(0, len(data), batch_size)]

with mp.Pool(processes=num_processes) as p:
    p.map(insert_batch, batches)