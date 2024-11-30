from datetime import date

import click


def validate_not_blank(ctx, param, value):
    """
    Проверяет вводимые поля на:
    - Поле не может состоять только из пробелов
    - Поле не может быть пустым
    """
    if value == "":
        raise click.BadParameter(
            f"Параметр '{param.name}' не может быть пустым."
        )
    if value is not None and value.isspace():
        raise click.BadParameter(
            f"Поле '{param.name}' не может состоять только из пробелов."
        )
    return value


def validate_date(ctx, param, value):
    """
    Проверяет вводимую дату на то, что указанное
    значение не раньше текущей даты.
    """
    if value is not None and value.date() < date.today():
        raise click.BadParameter("Дата не может быть раньше текущей.")
    return value
