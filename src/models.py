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
    element = CharField()
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


class MedalFactory:

    @classmethod
    def parse_multiplier(cls, multiplier_string):
        return [3.40, 3.40]

    @classmethod
    def medal(cls, medal_json):
        created_medal = Medal()

        # We only care about combat medals
        if not medal_json.get('type', None) == 'Combat':
            return None

        # Setting the required attributes. If any is empty, we won't create the medal
        try:
            created_medal.cost = medal_json['cost']
            created_medal.direction = medal_json['direction']
            created_medal.element = medal_json['element']
            created_medal.hits = medal_json['hits']
            created_medal.id = medal_json['id']
            created_medal.multiplier_min, created_medal.multiplier_max = cls.parse_multiplier(medal_json['multiplier'])
            created_medal.name = medal_json['name']
            created_medal.rarity = medal_json['rarity']
            created_medal.targets = medal_json['targets']
            created_medal.tier = medal_json['tier']
            created_medal.type = medal_json['type']

        except KeyError:
            return None
        
        created_medal.defence = medal_json.get('defence', None)
        created_medal.image_link = medal_json.get('image_link', None)
        created_medal.notes = medal_json.get('notes', None)
        created_medal.pullable = medal_json.get('pullable', None)
        created_medal.rarity = medal_json.get('rarity', None)
        created_medal.region = medal_json.get('region', None)
        created_medal.strength = medal_json.get('strength', None)
        created_medal.voice_link = medal_json.get('voice_link', None)

        created_medal.save()

        return created_medal