import json
from abc import ABC, abstractmethod
from datetime import date
from typing import Dict, List, Optional, TypedDict, TypeVar, Union

import click

from constants import (DEFAULT_STATUS_TASK,
                       DEFAULT_STATUS_TASK_FOR_UPDATE_STATUS)

T = TypeVar("T", bound="Task")


class TaskData(TypedDict):
    """
    Класс для более подробной аннотации типов данных для задачи.
    """
    id: int
    title: str
    description: str
    category: str
    due_date: str
    priority: str
    status: str


class TaskStorage(ABC):
    @abstractmethod
    def load_tasks(self) -> List[dict[str, Union[int, str]]]:
        """Загрузка всех задач.

        Returns:
            List[T]: список всех добавленных задач
        """
        pass

    @abstractmethod
    def save_tasks(self, tasks: List[T]) -> None:
        """Сохранение задач

        Args:
            tasks (List[T]): сохранение актуального списка задач
        """
        pass


class Task(ABC):
    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        due_date: str,
        category: str,
        priority: str,
        status: str,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.category = category
        self.priority = priority
        self.status = status

    @abstractmethod
    def display(self) -> str:
        """Возвращает задачу.

        Returns:
            str: Отображение задачи в консоли.
        """
        pass

    @abstractmethod
    def create_task(self) -> None:
        """Создание новой задачи."""
        pass


class TaskManager(ABC):
    def __init__(self, storage: TaskStorage, task: Task):
        self.storage = storage
        self.task = task

    @abstractmethod
    def view_tasks(self, category: Optional[str]) -> Union[List[Task], None]:
        """Возвращает список всех задач.

        Args:
            category (Optional[str]): Если передать название категории,
            то список будет отсортирован и будут выведены только задачи
            с указанной категорией
        """
        pass

    @abstractmethod
    def add_task(
        self,
        title: str,
        description: str,
        category: str,
        due_date: date,
        priority: str
    ) -> None:
        """Создает задачу с указанными аргументами

        Args:
            title (str): название задачи
            description (str): описание задачи
            category (str): категория задачи
            due_date (date): срок выполнения задачи
            priority (str): приоритет задачи.
        """
        pass

    @abstractmethod
    def delete_task(self, task_id: int, category: str) -> None:
        """Удаление задач в зависимости от аргумента.

        Args:
            task_id (int): удаление задачи с указанным ID
            category (str): удаление всех задач с указанной категорией
        Return: Если задача удалена успешно,
            будет выведено соотствующее информационное сообщение,
            в противном случае будет возвращена ошибка
        """
        pass

    @abstractmethod
    def edit_task(
        self,
        id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        category: Optional[str] = None,
        due_date: Optional[date] = None,
        priority: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Optional[T]:
        """Редактирование выбранной задачи.

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

        Returns:
            Optional[T]: Если ID указан верно, то вернется выбранная задача
                с измененными задачи, если ID указан не верно,
                то вернется ошибка
        """
        pass

    @abstractmethod
    def search_task(self, category: str, status: str) -> List[T]:
        pass


class FileTaskStorage(TaskStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def load_tasks(self) -> List[dict[str, Union[int, str]]]:
        """Возвращает список всех задач.

        Returns:
            List[dict[str, Union[int, str]]]: Список всех задач в
                формате списка словарей
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_tasks(self, tasks: List[dict[str, Union[int, str]]]) -> None:
        """Сохранение актуального списка задач.

        Args:
            tasks (List[dict[str, Union[int, str]]]): принимает актуальный
                список всех задач для сохранения
        """
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4, ensure_ascii=False)


class FileTask(Task):

    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        category: str,
        due_date: str,
        priority: str,
        status: str = DEFAULT_STATUS_TASK
    ):
        super().__init__(
            id, title, description, due_date, category, priority, status
        )

    def display(self) -> str:
        """Формат задачи для вывода в консоль.

        Returns:
            str: строка для вывода в консоль
        """
        return (
            f"ID: {self.id}\n"
            f"Название: {self.title}\n"
            f"Описание: {self.description}\n"
            f"Категория: {self.category}\n"
            f"Срок выполнения: {self.due_date}\n"
            f"Приоритет: {self.priority}\n"
            f"Статус: {self.status}\n"
        )

    def create_task(self) -> Dict[str, Union[str, int]]:
        """Создания словаря с данными из объекта класса
        для последующего сохранения задачи в JSON файл.

        Returns:
            Dict[str, Union[str, int]]: Возвращает словарь для
                сохранения в формате JSON
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": DEFAULT_STATUS_TASK,
        }


class FileTaskManager(TaskManager):
    """Класс для работы с задачами.

    Args:
        TaskManager (_type_): класс, от которого унаследован текущий класс
    """
    def __init__(
        self,
        storage: FileTaskStorage,
        task: type[FileTask]
    ):
        """Создает объект для работы с задачами.

        Args:
            storage (FileTaskStorage): указание класса используемого
                для хранения задач
            task (FileTask): указание класса используемого для работы с задачей
        """
        self.storage = storage
        self.task = task

    def view_tasks(self, category: Optional[str]) -> None:
        """Возвращает список всех задач.

        Args:
            category (Optional[str]): Если передать название категории,
            то список будет отсортирован и будут выведены только задачи
            с указанной категорией

        Returns: возвращает список всех подходящих под условия задач,
         если задачи отсутвуют вернется None
        """
        tasks = self.storage.load_tasks()

        # Получение списка задач, в зависимости от наличия передаваемого
        # аргумента, если параметр категория указан,
        # то список фильтруется по ней
        filter_tasks = (
            [self.task(**task) for task in tasks]
            if category is None
            else (
                [self.task(**task) for task in tasks
                 if task["category"] == category]
            )
        )

        if not filter_tasks:
            print("Нет задач.")
            return None

        # Вывод в консоль всех задач
        [print(task.display()) for task in filter_tasks]
        return None

    def add_task(
        self,
        title: str,
        description: str,
        category: str,
        due_date: date,
        priority: str
    ) -> None:
        """Создает задачу с указанными аргументами

        Args:
            title (str): название задачи
            description (str): описание задачи
            category (str): категория задачи
            due_date (date): срок выполнения задачи
            priority (str): приоритет задачи.
        """
        tasks = self.storage.load_tasks()

        # Вызов функции создания ID для записи
        task_id = self.create_id(tasks)
        # Форматирование даты в подходяший формат для записи в JSON
        due_date = due_date.date().isoformat()

        task = self.task(
            task_id, title, description, category, due_date, priority
        )
        tasks.append(self.task.create_task(task))

        self.storage.save_tasks(tasks)
        print("Задача добавлена.")

    def delete_task(self, task_id: int, category: str) -> None:
        """Удаление задач указанных в аргументе

        Args:
            task_id (int): удаление задачи с указанным ID
            category (str): удаление всех задач с указанной категорией
        Return: Если задача удалена успешно,
            будет выведено соотствующее информационное сообщение,
            в противном случае будет возвращена ошибка
        """
        if task_id and category:
            raise click.ClickException(
                "Можно указать только одну опцию: --id или --category."
            )
        tasks = self.storage.load_tasks()
        if task_id:
            # Поиск и удаление задачи с указанным ID
            try:
                task = next(task for task in tasks if task["id"] == task_id)
                tasks.remove(task)
            except StopIteration:
                raise click.ClickException("Задача с указанным ID не найдена.")
        else:
            # Поиск всех задач с указанной категорией
            new_tasks = [t for t in tasks if t["category"] != category]

            # Если длина не изменилась, значит ничего не удалили
            if len(tasks) == len(new_tasks):
                raise click.ClickException(
                    "Задачи с указанной категорией не найдены."
                )
            tasks = new_tasks

        self.storage.save_tasks(tasks)
        print("Успешное удаление.")

    def edit_task(
        self,
        id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        category: Optional[str] = None,
        due_date: Optional[date] = None,
        priority: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Optional[T]:
        """Редактирование выбранной задачи.

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

        Returns:
            Optional[T]: Если ID указан верно, то вернется выбранная задача
                с измененными задачи, если ID указан не верно,
                то вернется ошибка
        """
        tasks = self.storage.load_tasks()

        # Поиск задачи
        task = next((t for t in tasks if t["id"] == id), None)
        if not task:
            raise click.ClickException(f"Задача с ID {id} не найдена.")

        due_date = due_date.date().isoformat() if due_date else None

        # Обновление только измененных полей
        updates = {key: value for key, value in {
            "title": title,
            "description": description,
            "category": category,
            "due_date": due_date,
            "priority": priority,
            "status": status,
        }.items() if value is not None}

        task.update(updates)

        self.storage.save_tasks(tasks)
        print(f"Задача с ID {id} успешно обновлена.")
        task = self.task(**task)
        print(task.display())

    def search_task(self, category: str, status: str) -> None:
        """Поиск и вывод в консоль всех задач подходящих под условия поиска

        Args:
            status (str): будут найдены все задачи с указанным статусом
            category (str): будут найдены все задачи с подходящими категориями

        С помощью print() выводится список всех под
        """
        if status and category:
            raise click.ClickException(
                "Можно указать только одну опцию: --status или --category."
            )

        tasks = self.storage.load_tasks()

        if category:
            # Фильтрация задач по категории
            tasks = [
                self.task(**task)
                for task in tasks
                if category in task["category"]
            ]
            if not len(tasks):
                raise click.ClickException(
                    "Задачи с указанной категорией не найдены."
                )
        else:
            # Фильтрация задач по статусу
            tasks = [
                self.task(**task)
                for task in tasks
                if task["status"] == status
            ]
            if not len(tasks):
                raise click.ClickException(
                    "Задачи с указанным статусом не найдены."
                )

        # Вывод отфильтрованных задач в консоль
        for task in tasks:
            print(task.display())

    def update_status_task(self, id: int) -> None:
        """
        Изменение статуса задачи на 'Выполнена'.
        Если статус задачи уже отмечен этим статусом,
        будет возвращена ошибка с соответствующим сообщением

        Args:
            id (int): ID задачи для изменения статуса
        """
        tasks = self.storage.load_tasks()

        # Находим нужную задачу
        task = next((t for t in tasks if t["id"] == id), None)
        if not task:
            raise click.ClickException(f"Задача с ID {id} не найдена.")

        # Возвращаем ошибку, если задача уже имеет нудный статус
        if task["status"] == DEFAULT_STATUS_TASK_FOR_UPDATE_STATUS:
            raise click.ClickException(
                f"Задача с ID {id} уже отмечена как 'Выполнена'."
            )

        # Изменяем статус задачи
        task["status"] = DEFAULT_STATUS_TASK_FOR_UPDATE_STATUS

        self.storage.save_tasks(tasks)
        task = self.task(**task)
        print(task.display())

    @staticmethod
    def create_id(tasks: List[dict[str, Union[int, str]]]) -> int:
        """Создание ID для новой задачи.

        Args:
            tasks (List[dict[str, Union[int, str]]]): список всех задач
                для определения id

        Returns:
            int: возвращает ID для новой задачи
        """
        return tasks[-1]["id"] + 1 if tasks else 1
