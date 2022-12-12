import uuid
import datetime
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
# from app import IP, KEYSPACE
KEYSPACE = "movie_keyspace"
IP = '172.18.0.2'
connection.setup([IP], KEYSPACE, protocol_version=3)


class reviews(Model):
    user_name = columns.Text()
    review_id = columns.UUID(primary_key=True, default=uuid.uuid4())
    reviewer = columns.Text()
    movie = columns.Text()
    rating = columns.Integer()
    review_summary = columns.Text()
    review_date = columns.DateTime(default=datetime.datetime.now())
    # spoiler_tag = columns.Text()
    review_detail = columns.Text()
    helpful = columns.Text()
    created_at = columns.DateTime(default=datetime.datetime.now())

    def __repr__(self):
        return '%s %s %d' % (self.email, self.username, self.createdAt)


def sync_tabless():
    sync_table(reviews)
