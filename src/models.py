from peewee import *

db = PostgresqlDatabase(database='database_name', user='postgres',
                        password='secret', host='10.1.0.9', port=5432)

class BaseModel(Model):
    """Abstract model that we'll use to make other models inherit DB settings"""
    class Meta:
        database = db