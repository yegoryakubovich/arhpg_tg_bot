from peewee import MySQLDatabase

from config import MYSQL_NAME, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT

db = MySQLDatabase(
    database=MYSQL_NAME,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    charset='utf8mb4',
    autoconnect=False,
)
