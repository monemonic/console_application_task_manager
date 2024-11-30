import pytest

from commands import cli
from tests.utils import invalid_data


def test_add_task_success(runner, ctx, task_fixture, task_data):
    """Тест успешного добавления задачи."""
    # Проверяем, что в файле нет задач
    old_tasks = ctx.obj.storage.load_tasks()

    # Создаем новую задачу
    command = ["add-task"]
    args = command + task_fixture
    result = runner.invoke(cli, args, obj=ctx.obj)

    # Проверяем, что команда завершилась без ошибок
    assert result.exit_code == 0

    # Проверяем, что задача была добавлена в тестовый файл
    tasks = ctx.obj.storage.load_tasks()
    assert len(tasks) != len(old_tasks)

    # Проверяем, что все поля имеют ожидаемые значения.
    added_task = tasks[-1]
    test_fields = ("title", "description", "category", "due_date", "priority")
    for field in test_fields:
        assert added_task[field] == task_data[field]


@pytest.mark.parametrize("data", invalid_data)
def test_add_task_not_valid_fields(runner, ctx, data):
    """Тест добавления задачи с не валидными данными."""
    # Создаем новую задачу с невалидными данными
    command = ["add-task"]
    args = command + data
    result = runner.invoke(cli, args, obj=ctx.obj)

    # Проверяем, что команда завершилась с ошибкой
    assert result.exit_code == 2

    # Проверяем, что в файл не добавилось новых задач
    tasks = ctx.obj.storage.load_tasks()
    assert len(tasks) == 0


def test_view_tasks(
    runner, ctx, task_list,
    task_output_all_data, task_output_id_one
):
    """Тест правильного вывода списка задач."""
    # Проверка вывода всех добавленных задач
    command = ["view-tasks"]
    result = runner.invoke(cli, command, obj=ctx.obj)
    assert result.exit_code == 0
    assert task_output_all_data.strip() == result.output.strip()

    # Проверка вывода задач с указанием категории
    command = ["view-tasks", "--category", "Работа"]
    result = runner.invoke(cli, command, obj=ctx.obj)
    assert result.exit_code == 0
    assert task_output_id_one.strip() == result.output.strip()

    # Проверка вывода задач с указанием не существующий категории
    command = ["view-tasks", "--category", "Джобота"]
    result = runner.invoke(cli, command, obj=ctx.obj)
    assert result.exit_code == 0
    assert "Нет задач." == result.output.strip()


def test_delete_task_by_id(runner, ctx, task_list, task_output_id_one):
    """Тест правильности удаления задач с указанием ID."""
    # Находим изначальное количество добавленных задач.
    old_len_tasks = len(ctx.obj.storage.load_tasks())

    # Удаляем задачу, указывая ее ID
    command = ["delete-task", "--id", "2"]
    result = runner.invoke(cli, command, obj=ctx.obj)
    assert result.exit_code == 0

    # Проверяем, что задача действительно удалилась.
    new_len_tasks = len(ctx.obj.storage.load_tasks())
    assert old_len_tasks > new_len_tasks

    # Проверяем, что удалилась нужная задача.
    result = runner.invoke(cli, ["view-tasks"], obj=ctx.obj)
    assert task_output_id_one.strip() == result.output.strip()


def test_delete_task_by_category(
    runner, ctx, task_list, task_output_id_one
):
    """Тест правильности удаления задач с указанием категории."""
    # Находим изначальное количество добавленных задач.
    old_len_tasks = len(ctx.obj.storage.load_tasks())

    # Удаляем задачу, указывая ее ID
    command = ["delete-task", "--category", "Домашние"]
    result = runner.invoke(cli, command, obj=ctx.obj)
    assert result.exit_code == 0

    # Проверяем, что задача действительно удалилась.
    new_len_tasks = len(ctx.obj.storage.load_tasks())
    assert old_len_tasks > new_len_tasks

    # Проверяем, что удалилась нужная задача.
    result = runner.invoke(cli, ["view-tasks"], obj=ctx.obj)
    assert task_output_id_one.strip() == result.output.strip()


@pytest.mark.parametrize("data", invalid_data)
def test_edit_task_not_valid_data(
    runner, ctx, task_one, data, task_output_id_one
):
    """Тест попытки изменять поля задач не валидными данными."""
    command = ["edit-task", "--id", "1"]
    args = command + data
    result = runner.invoke(cli, args, obj=ctx.obj)
    # Проверяем, что команда завершилась с ошибкой
    assert result.exit_code == 2

    # Проверяем, что данные в задаче не изменились
    command = ["view-tasks"]
    task = runner.invoke(cli, command, obj=ctx.obj)
    assert task.exit_code == 0
    assert task_output_id_one.strip() == task.output.strip()


def test_edit_task_valid_data(
    runner, ctx, task_one,
    task_another_fixture, task_output_id_one_after_edit
):
    "Проверка изменения задачи валидными данными."
    # Получением изначальные данные задачи
    command = ["view-tasks"]
    result = runner.invoke(cli, command, obj=ctx.obj)
    assert result.exit_code == 0
    old_task_fields = result.output.strip()

    # Редактируем поля задачи
    command = ["edit-task", "--id", "1"]
    args = command + task_another_fixture
    result = runner.invoke(cli, args, obj=ctx.obj)
    assert result.exit_code == 0

    # Получением измененные данные задачи
    command = ["view-tasks"]
    result = runner.invoke(cli, command, obj=ctx.obj)
    assert result.exit_code == 0
    new_task_fields = result.output.strip()

    # Проверяем что поля изменились
    assert old_task_fields != new_task_fields

    # Проверяем, что данные сохранились верно
    assert task_output_id_one_after_edit.strip() == new_task_fields


def test_search_task(
    runner, ctx, task_list, task_output_id_one, task_output_id_two
):
    """Проверка поиска задач по ключевым словам."""
    # Выполняем поиск всех задач указанной категории
    command = ["search-task", "--category", "Работа"]
    result = runner.invoke(cli, command, obj=ctx.obj)
    assert result.exit_code == 0

    # Проверяем, что отобразились только те задачи,
    # которые соответствуют условию поиска
    assert task_output_id_one.strip() == result.output.strip()

    # Выполняем поиск всех задач с указанными статусом
    command = ["search-task", "--status", "Выполнена"]
    result = runner.invoke(cli, command, obj=ctx.obj)
    assert result.exit_code == 0

    # Проверяем, что отобразились только те задачи,
    # которые соответствуют условию поиска
    assert task_output_id_two.strip() == result.output.strip()

    # Выполняем поиск всех задач с ключевым словом,
    # которое не совпадет с имеющимися категориями
    command = ["search-task", "--category", "Космическая"]
    result = runner.invoke(cli, command, obj=ctx.obj)
    assert result.exit_code == 1

    # Проверяем, что запрос вернул ошибку с указанными значением
    assert (
        "Error: Задачи с указанной категорией не найдены."
        == result.output.strip()
    )


def test_update_status_task(
    runner, ctx, task_one, task_output_id_one_after_update_status
):
    """Проверка команды на изменение статуса задачи."""
    params = ["--id", "1"]

    # Получением изначальные данные задачи
    command = ["view-tasks"]
    result = runner.invoke(cli, command, obj=ctx.obj)
    assert result.exit_code == 0
    old_task_fields = result.output.strip()

    # Изменяем статус задачи
    command = ["update-status-task"] + params
    result = runner.invoke(cli, command, obj=ctx.obj)
    assert result.exit_code == 0
    new_task_fields = result.output.strip()

    # Проверяем что поля изменились
    assert old_task_fields != new_task_fields

    # Проверяем, что данные сохранились верно
    assert task_output_id_one_after_update_status.strip() == new_task_fields

    # Проверяем, что нельзя изменить статус у задач со статусом 'Выполнена'
    command = ["update-status-task"] + params
    result = runner.invoke(cli, command, obj=ctx.obj)
    assert result.exit_code == 1
    assert (
        f"Error: Задача с ID {params[-1]} уже отмечена как 'Выполнена'.\n"
        == result.output
    )

    # Проверяем, ответ, если указан не существующий ID
    command = ["update-status-task", "--id", "3"]
    result = runner.invoke(cli, command, obj=ctx.obj)
    assert result.exit_code == 1
    assert (
        f"Error: Задача с ID {command[-1]} не найдена.\n"
        == result.output
    )
