from khux_medal_finder import helpers
from khux_medal_finder.exceptions import ParseMultiplierError
from khux_medal_finder.models import Medal


class MedalFactory:

    @classmethod
    def parse_multiplier(cls, multiplier_string):
        try:
            processed_multiplier_string = helpers.prepare_multiplier_string(multiplier_string)
            multipliers = processed_multiplier_string.split('-')

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

        except (KeyError, ParseMultiplierError) as e:
            print(f"There has been an error while trying to create the medal: {repr(e)}")
            print(medal_json)
            return None

        created_medal.defence = medal_json.get('defence', None)
        created_medal.image_link = medal_json.get('image_link', None)
        created_medal.notes = medal_json.get('notes', None)
        created_medal.pullable = medal_json.get('pullable', None)
        created_medal.rarity = medal_json.get('rarity', None)
        created_medal.region = medal_json.get('region', None)
        created_medal.strength = medal_json.get('strength', None)
        created_medal.voice_link = medal_json.get('voice_link', None)

        if created_medal.save(force_insert=True):
            return created_medal