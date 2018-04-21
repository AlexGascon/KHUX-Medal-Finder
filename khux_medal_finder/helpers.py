def prepare_reply_body(medals):
    """Given a list of medals, returns a text string containing a comment
    reply with a table adequately formatted"""
    if not medals:
        raise ValueError("The medal list is empty")

    header_fields = ['Medal', 'Direction', 'Element', 'Targets', 'Multiplier',
                     'Tier', 'Hits', 'Notes']
    header = '|'.join(f'{field_name}' for field_name in header_fields)
    separator = ':--|' * len(header_fields)

    rows = []
    for medal in medals:
        attributes = [medal.name, medal.direction, medal.element, medal.targets,
                      prepare_multiplier(medal), medal.tier, medal.hits, medal.notes]
        row = '|'.join(str(attribute) for attribute in attributes)
        rows.append(row)

    return '\n'.join([header, separator, *rows[:10]])

def prepare_multiplier(medal):
    if medal.multiplier_min == medal.multiplier_max:
        return f'x{medal.multiplier_max}'
    else:
        return f'x{medal.multiplier_min} - {medal.multiplier_max}'