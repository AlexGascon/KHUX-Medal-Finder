def prepare_reply_body(medals):
    """Given a list of medals, returns a text string containing a comment
    reply with a table adequately formatted"""
    if not medals:
        raise ValueError("The medal list is empty")

    header_fields = ('Medal', 'Direction', 'Element', 'Targets', 'Multiplier', 'Tier', 'Hits', 'Notes')
    header = '|'.join(header_fields)

    header_separator = ':--|' * len(header_fields)

    rows = []
    # Include only 10 medals, to avoid generating a huge comment if the
    # requirements are generic
    for medal in medals[:10]:
        attributes = [medal.name, medal.direction, medal.element, medal.targets,
                      prepare_multiplier(medal), medal.tier, medal.hits, medal.notes]
        row = '|'.join(str(attribute) for attribute in attributes)
        rows.append(row)

    return '\n'.join((header, header_separator, *rows))

def prepare_multiplier(medal):
    if medal.multiplier_min == medal.multiplier_max:
        return f'x{medal.multiplier_max}'
    else:
        return f'x{medal.multiplier_min} - {medal.multiplier_max}'

def prepare_multiplier_string(input_multiplier_string):
    processed_multiplier_string = input_multiplier_string.strip()

    if processed_multiplier_string.lower().startswith('x'):
        processed_multiplier_string = processed_multiplier_string[1:]

    if '~' in processed_multiplier_string:
        processed_multiplier_string = processed_multiplier_string.replace('~', '-')

    return processed_multiplier_string