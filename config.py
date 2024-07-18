from dotenv import load_dotenv
import os

load_dotenv()

db_host = os.getenv('db_host')
db_port = os.getenv('db_port')
db_name = os.getenv('db_name')
db_user = os.getenv('db_user')
db_password = os.getenv('db_password')
database_uri_local = os.getenv('database_uri_local')
table_name = os.getenv('table_name')
connection_string = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
