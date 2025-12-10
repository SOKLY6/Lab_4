import random


class Player:
    """
    Класс игрока казино.

    Attributes:
        name: Имя игрока
        balance: Баланс игрока
    """

    def __init__(self, name: str, balance: int):
        """
        Инициализация игрока.

        Args:
            name: Имя игрока
            balance: Начальный баланс
        """
        self.name = name
        self.balance = balance


class Goose:
    """
    Базовый класс гуся.

    Attributes:
        name: Имя гуся
        honk_volume: Громкость гоготания
        balance: Баланс гуся (украденные деньги)
    """

    def __init__(self, name: str, honk_volume: int):
        """
        Инициализация гуся.

        Args:
            name: Имя гуся
            honk_volume: Громкость гоготания
        """
        self.name = name
        self.honk_volume = honk_volume
        self.balance = 0


class WarGoose(Goose):
    """Боевой гусь, способный воровать фишки."""

    def steal_chip(self) -> int:
        """
        Попытка украсть фишку.

        Returns:
            Случайное значение от 1 до 100 при успехе, 0 при неудаче
        """
        if (random.randint(1, 50) + self.honk_volume) > 30:
            return random.randint(1, 100)
        return 0


class HonkGoose(Goose):
    """Гогочущий гусь, способный пугать игроков громким криком."""

    def honk(self) -> int:
        """
        Попытка издать громкий крик.

        Returns:
            Громкость крика при успехе, 0 при неудаче
        """
        if random.randint(1, 100) > 20:
            return self.honk_volume
        return 0


class Chip:
    """
    Класс фишки казино.

    Attributes:
        colour: Цвет фишки
        value: Номинал фишки
    """

    def __init__(self, colour: str, value: int):
        """
        Инициализация фишки.

        Args:
            colour: Цвет фишки
            value: Номинал фишки
        """
        self.colour = colour
        self.value = value

    def __add__(self, add_value: int) -> 'Chip':
        """
        Увеличение номинала фишки.

        Args:
            add_value: Значение для добавления

        Returns:
            Сама фишка с обновленным номиналом
        """
        self.value += add_value
        return self
