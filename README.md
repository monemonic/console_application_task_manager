# Task CLI Manager

**Task CLI Manager** — это утилита для управления задачами через командную строку. Программа позволяет создавать, просматривать, редактировать, удалять и искать задачи, а также изменять их статус.

## Оглавление

- [Установка](#установка)
- [Использование](#использование)
  - [Просмотр задач](#просмотр-задач)
  - [Добавление задач](#добавление-задач)
  - [Редактирование задач](#редактирование-задач)
  - [Удаление задач](#удаление-задач)
  - [Поиск задач](#поиск-задач)
  - [Изменение статуса задач](#изменение-статуса-задач)
- [Требования](#требования)
- [Автор](#автор)

---

## Установка

1. Клонируйте репозиторий:

    ```bash
        git clone git@github.com:monemonic/console_application_task_manager.git
        cd console_application_task_manager
    ```

2. Установите зависимости:

    ```bash
        pip install -r requirements.txt
    ```

## Использование

### Просмотр задач
#### Просмотр всех задач:
    ```bash
        python commands.py view-tasks

    ```

#### Просмотр всех задач определенной категории:
    ```bash
        python commands.py view-tasks --category <категория>
    ```

### Добавление задач

    Для добавления новой задачи используется команда:

    ```bash
        python commands.py add-task
    ```

    Программа запросит следующие данные:

    - Название
    - Описание
    - Категория
    - Срок выполнения (в формате YYYY-MM-DD)
    - Приоритет (низкий, средний или высокий)

    При создании у задачи будет фиксированный статус "Не выполнена"

### Редактирование задач

    Редактирование существующей задачи:

    ```bash
        python commands.py edit-task --id <ID> [опции]
    ```

    Вы можете указать следующие опции:

    - --title — новое название
    - --description — новое описание
    - --category — новая категория
    - --due_date — новый срок выполнения (в формате YYYY-MM-DD)
    - --priority — новый приоритет
    - --status — новый статус

### Удаление задач

#### Удаление задач по ID:

    ```bash
        python commands.py delete-task --id <ID>
    ```

#### Удаление задач по категории:

    ```bash
        python commands.py delete-task --category <категория>
    ```

### Поиск задач

#### Поиск задач по статусу:

    ```bash
        python commands.py search-task --status <статус>
    ```

    Для поиска требуется указать полное название статуса

#### Поиск задач по категории:

    ```bash
        python commands.py search-task --category <категория>
    ```

    Будут показаны все задачи в которых присутствует указанная категория

### Изменение статуса задач

    Обновление статуса задачи на "Выполнена":

    ```bash
        python commands.py update-status-task --id <ID>
    ```

## Требования

    - Python 3.8 или выше
    - Библиотека Click
