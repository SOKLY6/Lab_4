from domain.casino_entities import Chip, Goose, HonkGoose, Player, WarGoose
from repository.base_classes import BaseCollection


class PlayerCollection(BaseCollection):
    """Коллекция игроков."""

    pass


class GooseCollection(BaseCollection):
    """Коллекция гусей."""

    pass


class ChipCollection(BaseCollection):
    """
    Коллекция фишек с предустановленными стандартными фишками.
    """

    def __init__(self) -> None:
        """Инициализация коллекции с 5 стандартными фишками."""
        self.items = [
            Chip('white', 1),
            Chip('green', 5),
            Chip('blue', 10),
            Chip('red', 25),
            Chip('black', 50),
        ]
        self.length = 5

    def add(self, item: Chip) -> None:
        """
        Добавление фишки в коллекцию с сортировкой по номиналу.

        Args:
            item: Фишка для добавления
        """
        self.items.append(item)
        self.length += 1
        sorted(self.items, key=lambda chip: chip.value)


class IndexDictChip:
    """
    Индексный словарь для поиска фишек по цвету.

    Attributes:
        dict_chip_value: Словарь сопоставления цвета и номинала фишки
    """

    def __init__(self) -> None:
        """Инициализация словаря со стандартными фишками."""
        self.dict_chip_value: dict[str, int] = {
            'white': 1,
            'green': 5,
            'blue': 10,
            'red': 25,
            'black': 50,
        }

    def add(self, chip: Chip) -> None:
        """
        Добавление фишки в индекс.

        Args:
            chip: Фишка для добавления

        Raises:
            ValueError: Если фишка с таким цветом или номиналом уже существует
        """
        for key, value in self.dict_chip_value.items():
            if chip.colour == key:
                raise ValueError('Такой цвет фишек уже есть')
            if chip.value == value:
                raise ValueError('Такой наминал фишек уже есть')
        self.dict_chip_value[chip.colour] = chip.value
        sorted(
            self.dict_chip_value,
            key=lambda colour: self.dict_chip_value[colour],
        )

    def pop(self, chip: Chip) -> None:
        """
        Удаление фишки из индекса.

        Args:
            chip: Фишка для удаления

        Raises:
            IndexError: Если фишка не найдена
        """
        if chip.colour not in self.dict_chip_value:
            raise IndexError('Такого цвета фишек нет, увы')
        else:
            self.dict_chip_value.pop(chip.colour)

    def search_chip_value(self, colour: str) -> int:
        """
        Поиск номинала фишки по цвету.

        Args:
            colour: Цвет фишки

        Returns:
            Номинал фишки

        Raises:
            IndexError: Если фишка не найдена
        """
        if colour not in self.dict_chip_value:
            raise IndexError('Такого вида фишек нет, увы')
        return self.dict_chip_value[colour]


class IndexDictPlayer:
    """
    Индексный словарь для поиска игроков по имени.

    Attributes:
        dict_player: Словарь сопоставления имени и игрока
    """

    def __init__(self) -> None:
        """Инициализация пустого словаря игроков."""
        self.dict_player: dict[str, Player] = {}

    def add(self, player: Player) -> None:
        """
        Добавление игрока в индекс.

        Args:
            player: Игрок для добавления

        Raises:
            ValueError: Если игрок с таким именем уже существует
        """
        if player in self.dict_player:
            raise ValueError('Игрок с таким именем уже есть')
        self.dict_player[player.name] = player

    def pop(self, player: Player) -> None:
        """
        Удаление игрока из индекса.

        Args:
            player: Игрок для удаления

        Raises:
            IndexError: Если игрок не найден
        """
        player_name = player.name
        if player_name not in self.dict_player and player_name not in self.dict_player:
            raise IndexError('Нет игрока с таким именем')
        self.dict_player.pop(player_name)

    def search_player(self, player_name: str) -> Player:
        """
        Поиск игрока по имени.

        Args:
            player_name: Имя игрока

        Returns:
            Объект игрока

        Raises:
            ValueError: Если игрок не найден
        """
        if player_name not in self.dict_player:
            raise ValueError('Игрока с таким именем нет')
        return self.dict_player[player_name]

    def search_player_balance(self, player_name: str) -> int:
        """
        Поиск баланса игрока по имени.

        Args:
            player_name: Имя игрока

        Returns:
            Баланс игрока

        Raises:
            ValueError: Если игрок не найден
        """
        if player_name not in self.dict_player:
            raise ValueError('Игрока с таким именем нет')
        return self.dict_player[player_name].balance


class IndexDictGoose:
    """
    Индексный словарь для поиска гусей по имени.

    Attributes:
        dict_war_goose: Словарь боевых гусей
        dict_honk_goose: Словарь гогочущих гусей
    """

    def __init__(self) -> None:
        """Инициализация пустых словарей гусей."""
        self.dict_war_goose: dict[str, WarGoose] = {}
        self.dict_honk_goose: dict[str, HonkGoose] = {}

    def add(self, goose: Goose) -> None:
        """
        Добавление гуся в соответствующий индекс.

        Args:
            goose: Гусь для добавления

        Raises:
            ValueError: Если гусь с таким именем уже существует
        """
        if isinstance(goose, WarGoose):
            if goose in self.dict_war_goose:
                ValueError('Гусь с таким именем уже есть')
            self.dict_war_goose[goose.name] = goose
        if isinstance(goose, HonkGoose):
            if goose in self.dict_honk_goose:
                ValueError('Гусь с таким именем уже есть')
            self.dict_honk_goose[goose.name] = goose

    def pop(self, goose: Goose) -> None:
        """
        Удаление гуся из индекса.

        Args:
            goose: Гусь для удаления

        Raises:
            ValueError: Если гусь не найден
        """
        goose_name = goose.name
        if (
            goose_name not in self.dict_war_goose
            and goose_name not in self.dict_honk_goose
        ):
            raise ValueError('Гуся с таким именем нет')
        if goose_name in self.dict_war_goose:
            self.dict_war_goose.pop(goose_name)
        if goose_name in self.dict_honk_goose:
            self.dict_honk_goose.pop(goose_name)

    def search_goose_balance(self, goose_name: str) -> int:
        """
        Поиск баланса гуся по имени.

        Args:
            goose_name: Имя гуся

        Returns:
            Баланс гуся

        Raises:
            ValueError: Если гусь не найден
        """
        if (
            goose_name not in self.dict_war_goose
            and goose_name not in self.dict_honk_goose
        ):
            raise ValueError('Гуся с таким именем нет')
        if goose_name in self.dict_war_goose:
            return self.dict_war_goose[goose_name].balance
        else:
            return self.dict_honk_goose[goose_name].balance

    def search_goose_honk_volume(self, goose_name: str) -> int:
        """
        Поиск громкости гоготания гуся по имени.

        Args:
            goose_name: Имя гуся

        Returns:
            Громкость гоготания

        Raises:
            ValueError: Если гусь не найден
        """
        if (
            goose_name not in self.dict_war_goose
            and goose_name not in self.dict_honk_goose
        ):
            raise ValueError('Гуся с таким именем нет')
        if goose_name in self.dict_war_goose:
            return self.dict_war_goose[goose_name].honk_volume
        else:
            return self.dict_honk_goose[goose_name].honk_volume

    def search_goose(self, goose_name: str) -> Goose:
        """
        Поиск гуся по имени.

        Args:
            goose_name: Имя гуся

        Returns:
            Объект гуся

        Raises:
            ValueError: Если гусь не найден
        """
        if (
            goose_name not in self.dict_war_goose
            and goose_name not in self.dict_honk_goose
        ):
            raise ValueError('Гуся с таким именем нет')
        if goose_name in self.dict_war_goose:
            return self.dict_war_goose[goose_name]
        else:
            return self.dict_honk_goose[goose_name]
