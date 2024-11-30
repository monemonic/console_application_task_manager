import click
import pytest
from click.testing import CliRunner

from classes import FileTask, FileTaskManager, FileTaskStorage
from commands import cli


@pytest.fixture
def task_fixture():
    return [
        "--title", "Моя задача",
        "--description", "Задача Тест",
        "--category", "Работа",
        "--due_date", "2025-12-12",
        "--priority", "низкий"
    ]


@pytest.fixture
def task_another_fixture():
    return [
        "--title", "Моя задача 2",
        "--description", "Задача Тест 2",
        "--category", "Домашние",
        "--due_date", "2029-12-12",
        "--priority", "высокий"
    ]


@pytest.fixture
def task_output_all_data():
    return (
        "ID: 1\n"
        "Название: Моя задача\n"
        "Описание: Задача Тест\n"
        "Категория: Работа\n"
        "Срок выполнения: 2025-12-12\n"
        "Приоритет: низкий\n"
        "Статус: Не выполнена\n\n"
        "ID: 2\n"
        "Название: Моя задача 2\n"
        "Описание: Задача Тест 2\n"
        "Категория: Домашние\n"
        "Срок выполнения: 2029-12-12\n"
        "Приоритет: высокий\n"
        "Статус: Выполнена\n"
    )


@pytest.fixture
def task_output_id_one():
    return (
        "ID: 1\n"
        "Название: Моя задача\n"
        "Описание: Задача Тест\n"
        "Категория: Работа\n"
        "Срок выполнения: 2025-12-12\n"
        "Приоритет: низкий\n"
        "Статус: Не выполнена\n\n"
    )


@pytest.fixture
def task_output_id_one_after_update_status():
    return (
        "ID: 1\n"
        "Название: Моя задача\n"
        "Описание: Задача Тест\n"
        "Категория: Работа\n"
        "Срок выполнения: 2025-12-12\n"
        "Приоритет: низкий\n"
        "Статус: Выполнена\n\n"
    )


@pytest.fixture
def task_output_id_one_after_edit():
    return (
        "ID: 1\n"
        "Название: Моя задача 2\n"
        "Описание: Задача Тест 2\n"
        "Категория: Домашние\n"
        "Срок выполнения: 2029-12-12\n"
        "Приоритет: высокий\n"
        "Статус: Не выполнена\n\n"
    )


@pytest.fixture
def task_output_id_two():
    return (
        "ID: 2\n"
        "Название: Моя задача 2\n"
        "Описание: Задача Тест 2\n"
        "Категория: Домашние\n"
        "Срок выполнения: 2029-12-12\n"
        "Приоритет: высокий\n"
        "Статус: Выполнена\n"
    )


@pytest.fixture
def task_data():
    return {
        "title": "Моя задача",
        "description": "Задача Тест",
        "category": "Работа",
        "due_date": "2025-12-12",
        "priority": "низкий"
    }


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def ctx(tmp_path):
    """Создание объекта контекста программы"""
    # Создаем временный файл для хранения задач
    test_file = tmp_path / "test_tasks.json"

    # Создаем экземпляры объектов для теста
    task_storage = FileTaskStorage(str(test_file))
    task_class = FileTask
    task_manager = FileTaskManager(task_storage, task_class)

    # Создаем объект контекста Click и передаем task_manager в obj
    ctx = click.Context(cli)
    ctx.obj = task_manager
    return ctx


@pytest.fixture
def task_one(ctx, runner, task_fixture):
    command = ["add-task"] + task_fixture
    runner.invoke(cli, command, obj=ctx.obj)


@pytest.fixture
def task_two(ctx, runner, task_another_fixture):
    command = ["add-task"] + task_another_fixture
    runner.invoke(cli, command, obj=ctx.obj)
    command = ["edit-task", "--id", "2", "--status", "Выполнена"]
    runner.invoke(cli, command, obj=ctx.obj)


@pytest.fixture
def task_list(ctx, runner, task_one, task_two):
    pass
