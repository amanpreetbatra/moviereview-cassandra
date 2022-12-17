from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.management import sync_type
from cassandra.cqlengine.management import drop_table

from models import reviews


def _setup_cassandra(hosts, keyspace):
    """Setup connection to cassandra nodes.
    This function needs to be called before making any queries.
    :param hosts `list`: list of hosts to connect to.
    :param keyspace `unicode`: name of the keyspace to connect.
    """
    if not isinstance(hosts, list):
        raise ValueError("hosts only accepts list of ips.")
    connection.setup(hosts=hosts, default_keyspace=keyspace,
                     protocol_version=3)


def setup_connections(config):
    """Set connection to Cassandra
    """
    keyspace = config.CASSANDRA_KEYSPACE
    hosts = config.CASSANDRA_HOSTS
    _setup_cassandra(hosts=hosts, keyspace=keyspace)

    sync_tables()


def sync_tables():
    """Sync all models to tables.
    """
    sync_table(Review)


def drop_tables():
    """Drop all tables in the keyspace.
    Note: Use this with care!.
    """
    drop_table(Review)
