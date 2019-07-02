
def one_or_many(items: list, default=''):
    """
    Taking a list as input,
    return the first item if there is only one item,
    else return the 'default' value is the list is empty,
    else return the initial list.
    """
    if items:
        if len(items) == 1:
            return items[0]
        return items
    return default
