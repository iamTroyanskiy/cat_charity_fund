def validate_positive_integer(key, value):
    if value <= 0:
        raise ValueError(f'Поле {key} должно быть больше 0!')
    return value
