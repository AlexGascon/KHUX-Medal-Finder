from peewee import *

db = PostgresqlDatabase(database='database_name', user='postgres',
                        password='secret', host='10.1.0.9', port=5432)

class BaseModel(Model):
    """Abstract model that we'll use to make other models inherit DB settings"""
    class Meta:
        database = db

class Medal(BaseModel):
    cost = IntegerField()
    defence = IntegerField()
    direction = CharField()
    hits = IntegerField()
    id = IntegerField(primary_key=True)
    image_link = TextField()
    multiplier_min = FloatField()
    multiplier_max = FloatField()
    name = TextField()
    notes = TextField()
    pullable = CharField(max_length=3)
    rarity = IntegerField()
    region = CharField(max_length=5)
    strength = IntegerField()
    targets = CharField(max_length=10)
    tier = IntegerField()
    type = CharField(max_length=10)
    voice_link = TextField()
