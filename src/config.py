import os

DB_CONNECTION = os.environ.get('DB_CONNECTION', 'postgres:pass@localhost:6789/postgres')
USER_EMAIL = os.environ.get('USER_EMAIL')
PASSWORD = os.environ.get('PASSWORD')
