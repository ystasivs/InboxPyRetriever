import re
import psycopg2
from config import DB_CONNECTION

CONNECTION_STRING_PATTERN = r'(.+):(.+)@(.+):(.+)/(.+)'
QUERY_INIT = """
    CREATE TABLE IF NOT EXISTS public.emails (
	id int4 NOT NULL,
	subject varchar NULL,
	sender varchar NULL,
	body text NULL,
	"date" varchar NULL,
	recipients varchar NULL,
	cc_recipients varchar NULL,
	bcc_recipients varchar NULL,
	CONSTRAINT emails_pk PRIMARY KEY (id)
);
"""
QUERY = (
    "INSERT INTO emails (id, subject, sender, body, date, recipients, cc_recipients, bcc_recipients) "
    "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
)


class DbStorage:
    def __init__(self):
        (
            self._user,
            self._password,
            self._host,
            self._port,
            self._database
        ) = re.search(CONNECTION_STRING_PATTERN, DB_CONNECTION).groups()
        print(self._user, self._host, self._password, self._port, self._database)

    def __enter__(self):
        self._conn = psycopg2.connect(database=self._database,
                                      host=self._host,
                                      user=self._user,
                                      password=self._password,
                                      port=self._port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.close()

    def save_to_db(self, emails):
        cursor = self._conn.cursor()
        cursor.executemany(QUERY, emails)
        self._conn.commit()

    def initialize_db(self):
        try:
            cursor = self._conn.cursor()
            cursor.execute(QUERY_INIT)
            self._conn.commit()
        except Exception as e:
            print(f'Error: {e}')
