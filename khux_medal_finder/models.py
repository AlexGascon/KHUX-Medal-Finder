import os
from peewee import *
from khux_medal_finder.exceptions import ParseMultiplierError

db = PostgresqlDatabase(database=os.environ['DB_DATABASE'],
                        user=os.environ['DB_USERNAME'],
                        password=os.environ['DB_PASSWORD'],
                        host=os.environ['DB_HOST'],
                        port=os.environ['DB_PORT'],
                        autorollback=True)


class BaseModel(Model):
    """Abstract model that we'll use to make other models inherit DB settings"""
    class Meta:
        database = db


class Medal(BaseModel):
    cost = IntegerField()
    defence = IntegerField(null=True)
    direction = CharField()
    element = CharField()
    hits = IntegerField()
    image_link = TextField(null=True)
    medal_id = IntegerField(primary_key=True, index=True)
    multiplier_min = FloatField()
    multiplier_max = FloatField()
    name = TextField(index=True)
    notes = TextField(null=True)
    pullable = CharField(max_length=3, null=True)
    rarity = IntegerField(null=True)
    region = CharField(max_length=5, null=True)
    strength = IntegerField(null=True)
    targets = CharField(max_length=10)
    tier = IntegerField()
    type = CharField(max_length=10)
    voice_link = TextField(null=True)


class MedalFactory:

    @classmethod
    def parse_multiplier(cls, multiplier_string):
        try:
            multipliers = multiplier_string.split('-')

            if multipliers[0].startswith('x'):
                multipliers[0] = multipliers[0][1:]

            if len(multipliers) == 1:
                multipliers = [multipliers[0]] * 2

            return list(map(float, multipliers))

        except Exception:
            raise ParseMultiplierError(f"The value {multiplier_string} couldn't be parsed")

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
            created_medal.medal_id = medal_json['id']
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

        created_medal.save(force_insert=True)

        return created_medal


class Comment(BaseModel):
    """Comment posted by a user on Reddit"""
    author = CharField()
    comment_id = CharField()
    text = TextField()
    timestamp = TimestampField()
    url = CharField(max_length=400)


class Reply(Comment):
    """Reply made by the bot to one Reddit comment. Though it could be modelled
    using Comment, this allows us to extend its functionality"""
    author = CharField(default=lambda: 'khux_medal_finder')
    original_comment = ForeignKeyField(Comment)
    success = BooleanField()
