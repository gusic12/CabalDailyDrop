

def convert_value(value):
    multipliers = {'k': 1_000, 'm': 1_000_000, 'b': 1_000_000_000}
    value = value.lower().replace(',', '.')

    if any(char in value for char in multipliers.keys()):
        for char, multiplier in multipliers.items():
            if char in value:
                return int(float(value.replace(char, '')) * multiplier)
    return int(value)


def convert_number(number):
    if number >= 1_000_000_000:
        formatted_number = number / 1_000_000_000
        return f'{formatted_number:.2f}b' if formatted_number % 1 != 0 else f'{int(formatted_number)}b'
    elif number >= 1_000_000:
        formatted_number = number / 1_000_000
        return f'{formatted_number:.2f}m' if formatted_number % 1 != 0 else f'{int(formatted_number)}m'
    elif number >= 1_000:
        formatted_number = number / 1_000
        return f'{formatted_number:.2f}k' if formatted_number % 1 != 0 else f'{int(formatted_number)}k'
    else:
        return str(int(number)) if number % 1 == 0 else str(number)



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


def get_color(value):
    if value >= 1_000_000_000:
        return 'lightblue'
    elif value >= 100_000_000:
        return 'orange'
    elif value >= 10_000_000:
        return 'green'
    elif value >= 1_000_000:
        return 'lightblue'
    else:
        return 'yellow'
