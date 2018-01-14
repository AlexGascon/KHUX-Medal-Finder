def extract_filters(comment):
    """Given a comment, returns a dict with the filters specified on it"""
    search_filters = {}
    comment = comment.lower()

    # Direction
    if "upright" in comment:
        search_filters["direction"] = "Upright"

    if "reversed" in comment:
        search_filters["direction"] = "Reversed"

    # Element
    elements = []
    if "power" in comment:
        elements.append("Power")

    if "speed" in comment:
        elements.append("Speed")

    if "magic" in comment:
        elements.append("Magic")

    if len(elements) == 1:
        search_filters["element"] = elements[0]
    elif len(elements) > 1:
        search_filters["element"] = elements

    # Element
    targets = []
    if "single" in comment:
        targets.append("Single")

    if "aoe" in comment:
        targets.append("All")

    if "random" in comment:
        targets.append("Random")

    if len(targets) == 1:
        search_filters["targets"] = targets[0]
    elif len(targets) > 1:
        search_filters["targets"] = targets

    return search_filters
