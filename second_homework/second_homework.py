def get_price(shrubbery):
    total_cost = 0

    for item in shrubbery['positional']:
        if 'cost' in item:
            total_cost += item['cost']

    for value in shrubbery['named'].values():
        if 'cost' in value:
            total_cost += value['cost']

    return total_cost


def get_all_valid_shrubs(*args, **kwargs):
    valid_bush_names = ("храст", "shrub", "bush")
    valid_shrubs = {'positional': [], 'named': {}}

    for arg in args:
        if (isinstance(arg, dict)
                and 'name' in arg
                and arg.get('name').lower() in valid_bush_names):
            valid_shrubs['positional'].append(arg)

    for key, value in kwargs.items():
        if (isinstance(value, dict)
                and 'name' in value
                and value.get('name').lower() in valid_bush_names):
            valid_shrubs['named'][key] = value

    return valid_shrubs


def function_that_says_ni(*args, **kwargs):
    shrubbery_max_price = 42
    shrubbery = get_all_valid_shrubs(*args,**kwargs)
    shrubbery_price = get_price(shrubbery)

    if shrubbery_price > shrubbery_max_price:
        return 'Ni!'

    unique_symbols = set(''.join(str(key) for key in shrubbery['named']))

    if shrubbery_price == 0 or len(unique_symbols) % int(shrubbery_price) != 0:
        return 'Ni!'

    return f"{shrubbery_price:.2f}лв"