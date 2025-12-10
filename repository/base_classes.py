from typing import Any


class BaseCollection:
    """
    Базовый класс коллекции с основными операциями.

    Attributes:
        items: Список элементов коллекции
        length: Количество элементов в коллекции
    """

    def __init__(self) -> None:
        """Инициализация пустой коллекции."""
        self.items: list[Any] = []
        self.length = 0

    def __getitem__(self, key: int | slice) -> Any | list[Any]:
        """
        Получение элемента по индексу или срезу.

        Args:
            key: Индекс элемента или срез

        Returns:
            Элемент или список элементов
        """
        return self.items[key]

    def __iter__(self) -> Any:
        """
        Инициализация итератора.

        Returns:
            Сам объект как итератор
        """
        self.index = -1
        return self

    def __next__(self) -> Any:
        """
        Получение следующего элемента при итерации.

        Returns:
            Следующий элемент коллекции

        Raises:
            StopIteration: Если достигнут конец коллекции
        """
        if self.index + 1 < self.length:
            self.index += 1
            return self.items[self.index]
        else:
            raise StopIteration

    def __len__(self) -> int:
        """
        Получение длины коллекции.

        Returns:
            Количество элементов в коллекции
        """
        return self.length

    def add(self, item: Any) -> None:
        """
        Добавление элемента в коллекцию.

        Args:
            item: Элемент для добавления
        """
        self.length += 1
        self.items.append(item)

    def pop(self, index: int | None = None) -> Any:
        """
        Удаление и возврат элемента из коллекции.

        Args:
            index: Индекс элемента для удаления. Если None, удаляется последний элемент

        Returns:
            Удаленный элемент

        Raises:
            IndexError: Если коллекция пуста
        """
        if not self.items:
            raise IndexError('Элементов в коллекции нет')
        if index is None:
            index = self.length - 1
        self.length -= 1
        deleted_item = self.items.pop(index)
        return deleted_item
