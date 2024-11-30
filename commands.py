
from datetime import date
from typing import Optional

import click

from classes import FileTask, FileTaskManager, FileTaskStorage
from constants import PRIORITY_TYPE, TASK_STATUS
from validators import validate_date, validate_not_blank


@click.group()
@click.pass_context
def cli(ctx):
    """
    Базовая группа команд для управления задачами.

    Инициализирует CLI и передает объект контекста (ctx),
    содержащий экземпляры:
    FileTaskManager, связанный с хранилищем задач.
    """
    pass


@cli.command()
@click.pass_context
@click.option(
    "--category",
    default=None,
    help="Категория задач для отображения."
)
def view_tasks(
    ctx,
    category: Optional[str]
) -> None:
    """Команда для просмотра задач.

    Args:
        category (Optional[str]): при указании категории,
            записи будут отфильтрованы и выведены только
            задачи с указанной категорией
    """
    task_manager = ctx.obj
    task_manager.view_tasks(category)


@cli.command()
@click.pass_context
@click.option(
    "--title",
    prompt="Название",
    callback=validate_not_blank,
    type=str,
    help="Название задачи",
)
@click.option(
    "--description",
    prompt="Описание",
    type=str,
    callback=validate_not_blank,
    help="Описание задачи",
)
@click.option(
    "--category",
    prompt="Категория",
    type=str,
    callback=validate_not_blank,
    help="Категория задачи",
)
@click.option(
    "--due_date",
    prompt="Срок выполнения (YYYY-MM-DD)",
    help="Срок задачи",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    callback=validate_date
)
@click.option(
    "--priority",
    prompt="Приоритет",
    type=click.Choice(PRIORITY_TYPE),
    help="Приоритет задачи",
)
def add_task(
    ctx,
    title: str,
    description: str,
    category: str,
    due_date: date,
    priority: str
) -> None:
    """Команда для создания новой задачи.

    Validators:
        Поля title, description, category проверяются валидатором на то,
            что строка не состоит полностью из пробелов
        Поле due_date, проверяется на то, является ли вводимое значение датой
            и дата выполнения больше текущей даты

    Args:
        title (str): название
        description (str): описание
        category (str): категория
        due_date (date): дата выполнения
        priority (str): приоритет
    """

    task_manager = ctx.obj
    task_manager.add_task(title, description, category, due_date, priority)


@cli.command()
@click.pass_context
@click.option(
    "--id",
    type=int,
    help="Удалить задачу по ID."
)
@click.option(
    "--category",
    type=str,
    callback=validate_not_blank,
    help="Удалить задачи по категории."
)
def delete_task(
    ctx,
    id: Optional[int],
    category: Optional[str]
) -> None:
    """
    Команда для удаления записи, требует ID или категорию
    задачи в качестве аргумента. Оба аргумента опциональны,
    но для успешной работы должен быть указан хотя бы один из них

    Args:
        id (Optional[int]): будет удалена задача с указанными ID
        category (Optional[str]): будут удалены все задачи
            с указанной категорией
    """
    task_manager = ctx.obj
    task_manager.delete_task(id, category)


@cli.command()
@click.pass_context
@click.option(
    "--id",
    type=int,
    required=True,
    help="ID задачи для редактирования."
)
@click.option(
    "--title",
    type=str,
    callback=validate_not_blank,
    help="Отредактированное название задачи"
)
@click.option(
    "--description",
    type=str,
    callback=validate_not_blank,
    help="Отредактированное описание задачи"
)
@click.option(
    "--category",
    type=str,
    callback=validate_not_blank,
    help="Отредактированная категория задачи",
)
@click.option(
    "--due_date",
    help="Отредактированный срок задачи",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    callback=validate_date
)
@click.option(
    "--priority",
    type=click.Choice(PRIORITY_TYPE),
    help="Отредактированный приоритет задачи",
)
@click.option(
    "--status",
    type=click.Choice(TASK_STATUS),
    help="Отредактированный статус задачи"
)
def edit_task(
    ctx,
    id: int,
    title: Optional[str],
    description: Optional[str],
    category: Optional[str],
    due_date: Optional[date],
    priority: Optional[str],
    status: Optional[str]
) -> None:
    """
     Команда для редактирования выбранной задачи.

     Validators:
        Поля title, description, category проверяются валидатором на то,
            что строка не состоит полностью из пробелов
        Поле due_date, проверяется на то, что дата
            выполнения обязательно больше текущей даты

    Args:
        id (int): обязательное поле, указывает задачу для редактирования
        title (Optional[str], optional): опциальное поле названия задачи
            для редактирования, если не указать будет равно None.
        description (Optional[str], optional): опциальное поле описания
            задачи для редактирования, если не указать будет равно None.
        category (Optional[str], optional): опциальное поле категории
            задачи для редактирования, если не указать будет равно None.
        due_date (Optional[date], optional): опциальное поле срока
            выполнения задачи для редактирования, если не указать
            будет равно None.
        priority (Optional[str], optional): опциальное поле приоритетности
            задачи для редактирования, если не указать будет равно None.
        status (Optional[str], optional): опциальное поле статуса задачи
            для редактирования, если не указать будет равно None.

    """
    task_manager = ctx.obj
    print(id, title, description, category, due_date, priority, status)
    task_manager.edit_task(
        id, title, description, category, due_date, priority, status
    )


@cli.command()
@click.pass_context
@click.option(
    "--status",
    type=str,
    help="Найти все задачи по  указанному статусу."
)
@click.option(
    "--category",
    type=str,
    callback=validate_not_blank,
    help="Найти все задачи по  указанной категории."
)
def search_task(
    ctx,
    status: Optional[str],
    category: Optional[str]
) -> None:
    """
    Команда для поиска всех записей удовлетворяющих критериям поиска,
    требует статус или категорию задачи в качестве аргумента.
    Оба аргумента опциональны, но для успешной работы должен
    быть указан хотя бы один из них

    Args:
        status (Optional[int]): будут показаны все задачи с указанным статусом
        category (Optional[str]): будут показаны все задачи
            с указанной категорией
    """
    task_manager = ctx.obj
    task_manager.search_task(
        category, status
    )


@cli.command()
@click.pass_context
@click.option(
    "--id",
    type=int,
    required=True,
    help="ID задачи для изменения статуса на 'Выполнена'."
)
def update_status_task(
    ctx,
    id: int
) -> None:
    """
    Команла для изменения статуса задачи на 'Выполнена'

    Args:
        id (int): обязательное поле, указывает задачу для изменения статуса
    """
    task_manager = ctx.obj
    task_manager.update_status_task(id)


if __name__ == "__main__":
    task_storage = FileTaskStorage("tasks.json")
    task_class = FileTask
    task_manager = FileTaskManager(task_storage, task_class)

    cli(obj=task_manager)
