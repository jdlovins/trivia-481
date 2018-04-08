def to_camel_case(snake_str):
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])


def ordinal(num):
    return "%d%s" % (num, "tsnrhtdd"[(num / 10 % 10 != 1) * (num % 10 < 4) * num % 10::4])

