# __created_by__ == Paul Patterson
from lib.database_connection import DatabaseConnection

connection = DatabaseConnection(test_mode=False)
connection.connect()
connection.seed("seeds/makersbnb.sql")
