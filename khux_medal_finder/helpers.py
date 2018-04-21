def prepare_reply_body(medals):
    """Given a list of medals, returns a text string containing a comment
    reply with a table adequately formatted"""
    if not medals:
        raise ValueError("The medal list is empty")

    header_fields = ['Medal', 'Direction', 'Element', 'Targets', 'Multiplier',
                     'Tier', 'Hits', 'Notes']
    header = (f'{field_name}' for field_name in header_fields).join('|')
    separator = (':--|' * len(header_fields)).join('|')

    rows = []
    for medal in medals:
        attributes = [medal.name, medal.direction, medal.element, medal.targets,
                      prepare_multiplier(medal), medal.tier, medal.hits, medal.notes]
        row = attributes.join('|')
        rows.append(row)

    return [header, separator, *rows[:10]].join('\n')

def prepare_multiplier(medal):
    if medal.multiplier_min == medal.multiplier_max:
        return f'x{multplier.max}'
    else:
        return f'x{medal.multiplier_min} - {medal.multiplier_max}'