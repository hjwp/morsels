
def deep_flatten(thing):
    if not hasattr(thing, "__iter__"):
        return [thing]

    if isinstance(thing, str):
        return [thing]

    flattened = []
    for item in thing:
        flattened.extend(deep_flatten(item))
    return flattened
