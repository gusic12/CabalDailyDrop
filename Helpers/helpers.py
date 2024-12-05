

def convert_value(value):
    multipliers = {'k': 1_000, 'm': 1_000_000, 'b': 1_000_000_000}
    value = value.lower().replace(',', '.')

    if any(char in value for char in multipliers.keys()):
        for char, multiplier in multipliers.items():
            if char in value:
                return int(float(value.replace(char, '')) * multiplier)
    return int(value)


def format_value(value):
    if value >= 1_000_000_000:
        formatted_value = value / 1_000_000_000
        return f"{formatted_value:.1f}".rstrip('0').rstrip('.') + 'b'
    elif value >= 1_000_000:
        formatted_value = value / 1_000_000
        return f"{formatted_value:.1f}".rstrip('0').rstrip('.') + 'm'
    elif value >= 1_000:
        formatted_value = value / 1_000
        return f"{formatted_value:.1f}".rstrip('0').rstrip('.') + 'k'
    return str(value)
