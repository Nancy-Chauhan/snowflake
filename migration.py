# track which SQL scripts are already applied
import datetime
import logging
import os
from dataclasses import dataclass
from urllib.parse import urlparse

import psycopg2
import sys
from dotenv import load_dotenv

logging.basicConfig(level=os.getenv('LOG_LEVEL', logging.INFO))

log = logging.getLogger('migration')


def open_connection():
    load_dotenv()
    uri = os.getenv('DATABASE_URI')

    if uri is None:
        log.error('DATABASE_URI not defined, exiting')
        sys.exit(1)

    result = urlparse(uri)  # also in python 3+ use: urlparse("YourUrl") not urlparse.urlparse("YourUrl")
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname

    return psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=hostname
    )


@dataclass
class Migration:
    version: int
    description: str
    script: str


def load_migrations(directory='migrations'):
    files = os.listdir(directory)

    migrations = []

    for file in files:
        if not file.endswith('.sql'):
            continue

        file_name = os.path.splitext(file)[0]
        version, description = file_name.split('_', 1)

        with open(os.path.join(directory, file)) as f:
            script = f.read()

            migrations.append(Migration(version=int(version), description=description, script=script))

    migrations.sort(key=lambda m: m.version)

    return migrations


def migrate():
    with open_connection() as conn:
        with conn.cursor() as c:
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS migrations (
                   id SERIAL PRIMARY KEY,
                   version INTEGER NOT NULL,
                   description TEXT,
                   applied_at TIMESTAMP NOT NULL)
                """)

            c.execute('SELECT version FROM migrations')
            rows = c.fetchall()

            applied_versions = set([row[0] for row in rows])

            migrations = load_migrations()

            for migration in migrations:
                if migration.version not in applied_versions:
                    log.info('Applying %s', migration.script)
                    c.execute(migration.script)

                    c.execute('INSERT INTO migrations(version, description, applied_at) VALUES (%s, %s, %s)',
                              (migration.version, migration.description, datetime.datetime.now()))
                    log.info('Applied %s %s', migration.version, migration.description)

            print("Applied migrations")


if __name__ == '__main__':
    migrate()
