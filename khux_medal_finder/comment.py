class RequirementExtractor:

    def __init__(self, comment):
        self.comment = comment.lower()
        self.requirements = {}

    def extract_requirements(self):
        self.requirements['elements'] = self.parse_element()
        self.requirements['targets'] = self.parse_targets()
        self.requirements['direction'] = self.parse_direction()

    def parse_element(self):
        elements = []

        if 'power' in self.comment:
            elements.append('Power')

        if 'speed' in self.comment:
            elements.append('Speed')

        if 'magic' in self.comment:
            elements.append('Magic')

        if 'psm' in self.comment:
            elements = ['Power', 'Magic', 'Speed']

        return elements

    def parse_targets(self):
        targets = []

        if 'single' in self.comment:
            targets.append('Single')

        if 'random' in self.comment:
            targets.append('Random')

        if any(word in self.comment for word in ['aoe', 'multi']):
            targets.append('All')

        return targets

    def parse_direction(self):
        direction = []

        if 'upright' in self.comment:
            direction.append('Upright')

        if 'reversed' in self.comment:
            direction.append('Reversed')

        return direction