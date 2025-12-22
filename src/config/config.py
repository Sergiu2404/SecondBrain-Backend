import os
from dotenv import load_dotenv

load_dotenv()

PG_USERNAME = os.getenv('PG_USERNAME')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_PORT = os.getenv('PG_PORT')
PG_DB = os.getenv('PG_DB')

PG_CONNECTION_STRING = f"postgresql://{PG_USERNAME}:{PG_PASSWORD}@localhost:{PG_PORT}/{PG_DB}"