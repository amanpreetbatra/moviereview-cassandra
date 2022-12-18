import uuid
import datetime
import os
from dotenv import load_dotenv
load_dotenv()
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table

# from app import IP, KEYSPACE
KEYSPACE = "movie_keyspace"
IP = os.getenv('IP_ADDRESS')
connection.setup([IP], KEYSPACE, protocol_version=3)


class reviews(Model):
    review_id = columns.Text(primary_key=True, default=uuid.uuid4())
    reviewer = columns.Text()
    movie = columns.Text()
    rating = columns.Text()
    review_summary = columns.Text()
    review_date = columns.Text()
    spoiler_tag = columns.Integer()
    review_detail = columns.Text()
    helpful = columns.List(value_type=columns.Integer())

    def __repr__(self):
        return '%s %s %s' % (self.review_id, self.reviewer, self.review_date)


def sync_tabless():
    sync_table(reviews)
