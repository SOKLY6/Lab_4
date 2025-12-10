import random

from domain.casino_entities import Chip, Goose, HonkGoose, Player, WarGoose
from repository.casino_collections import (
    ChipCollection,
    GooseCollection,
    IndexDictChip,
    IndexDictGoose,
    IndexDictPlayer,
    PlayerCollection,
)


class Casino:
    """
    Класс казино для управления игроками, гусями и фишками.

    Attributes:
        chip_collection: Коллекция фишек
        player_collection: Коллекция игроков
        goose_collection: Коллекция гусей
        index_dict_chip: Индекс для поиска фишек
        index_dict_player: Индекс для поиска игроков
        index_dict_goose: Индекс для поиска гусей
    """

    def __init__(
        self,
        chip_collection: ChipCollection,
        player_collection: PlayerCollection,
        goose_collection: GooseCollection,
        index_dict_chip: IndexDictChip,
        index_dict_player: IndexDictPlayer,
        index_dict_goose: IndexDictGoose,
    ) -> None:
        """
        Инициализация казино.

        Args:
            chip_collection: Коллекция фишек
            player_collection: Коллекция игроков
            goose_collection: Коллекция гусей
            index_dict_chip: Индекс фишек
            index_dict_player: Индекс игроков
            index_dict_goose: Индекс гусей
        """
        self.chip_collection = chip_collection
        self.player_collection = player_collection
        self.goose_collection = goose_collection
        self.index_dict_chip = index_dict_chip
        self.index_dict_player = index_dict_player
        self.index_dict_goose = index_dict_goose

    def add_chip(self, chip: Chip) -> None:
        """
        Добавление фишки в казино.

        Args:
            chip: Фишка для добавления
        """
        self.chip_collection.add(chip)
        self.index_dict_chip.add(chip)

    def add_player(self, player: Player) -> None:
        """
        Добавление игрока в казино.

        Args:
            player: Игрок для добавления
        """
        self.player_collection.add(player)
        self.index_dict_player.add(player)

    def add_goose(self, goose: Goose) -> None:
        """
        Добавление гуся в казино.

        Args:
            goose: Гусь для добавления
        """
        self.goose_collection.add(goose)
        self.index_dict_goose.add(goose)

    def pop_chip(self, index: int) -> Chip:
        """
        Удаление и возврат фишки по индексу.

        Args:
            index: Индекс фишки (нумерация с 1)

        Returns:
            Удаленная фишка
        """
        deleted_chip = self.chip_collection.pop(index - 1)
        self.index_dict_chip.pop(deleted_chip)
        return deleted_chip

    def pop_player(self, index: int) -> Player:
        """
        Удаление и возврат игрока по индексу.

        Args:
            index: Индекс игрока (нумерация с 1)

        Returns:
            Удаленный игрок
        """
        deleted_player = self.player_collection.pop(index - 1)
        self.index_dict_player.pop(deleted_player)
        return deleted_player

    def pop_goose(self, index: int) -> Goose:
        """
        Удаление и возврат гуся по индексу.

        Args:
            index: Индекс гуся (нумерация с 1)

        Returns:
            Удаленный гусь
        """
        deleted_goose = self.goose_collection.pop(index - 1)
        self.index_dict_goose.pop(deleted_goose)
        return deleted_goose

    def iter_chip(self) -> list[Chip]:
        """
        Получение итератора по фишкам.

        Returns:
            Итератор коллекции фишек
        """
        return iter(self.chip_collection)

    def iter_player(self) -> list[Player]:
        """
        Получение итератора по игрокам.

        Returns:
            Итератор коллекции игроков
        """
        return iter(self.player_collection)

    def iter_goose(self) -> list[Goose]:
        """
        Получение итератора по гусям.

        Returns:
            Итератор коллекции гусей
        """
        return iter(self.goose_collection)

    def get_chip_slice(self, key: int | slice) -> Chip | list[Chip]:
        """
        Получение фишки или среза фишек.

        Args:
            key: Индекс или срез

        Returns:
            Фишка или список фишек
        """
        return self.chip_collection.__getitem__(key)

    def get_player_slice(self, key: int | slice) -> Player | list[Player]:
        """
        Получение игрока или среза игроков.

        Args:
            key: Индекс или срез

        Returns:
            Игрок или список игроков
        """
        return self.player_collection.__getitem__(key)

    def get_goose_slice(self, key: int | slice) -> Goose | list[Goose]:
        """
        Получение гуся или среза гусей.

        Args:
            key: Индекс или срез

        Returns:
            Гусь или список гусей
        """
        return self.goose_collection.__getitem__(key)

    def search_chip_value(self, colour: str) -> int:
        """
        Поиск номинала фишки по цвету.

        Args:
            colour: Цвет фишки

        Returns:
            Номинал фишки
        """
        return self.index_dict_chip.search_chip_value(colour)

    def search_player(self, player_name: str) -> Player:
        """
        Поиск игрока по имени.

        Args:
            player_name: Имя игрока

        Returns:
            Объект игрока
        """
        return self.index_dict_player.search_player(player_name)

    def search_player_balance(self, player_name: str) -> int:
        """
        Поиск баланса игрока по имени.

        Args:
            player_name: Имя игрока

        Returns:
            Баланс игрока
        """
        return self.index_dict_player.search_player_balance(player_name)

    def search_goose(self, goose_name: str) -> Goose:
        """
        Поиск гуся по имени.

        Args:
            goose_name: Имя гуся

        Returns:
            Объект гуся
        """
        return self.index_dict_goose.search_goose(goose_name)

    def search_goose_balance(self, goose_name: str) -> int:
        """
        Поиск баланса гуся по имени.

        Args:
            goose_name: Имя гуся

        Returns:
            Баланс гуся
        """
        return self.index_dict_goose.search_goose_balance(goose_name)

    def search_goose_honk_volume(self, goose_name: str) -> int:
        """
        Поиск громкости гоготания гуся по имени.

        Args:
            goose_name: Имя гуся

        Returns:
            Громкость гоготания
        """
        return self.index_dict_goose.search_goose_honk_volume(goose_name)

    def war_goose_steal_chip(self, goose_name: str, player_name: str) -> Chip:
        """
        Боевой гусь пытается украсть фишку у игрока.

        Args:
            goose_name: Имя боевого гуся
            player_name: Имя игрока-жертвы

        Returns:
            Украденная фишка

        Raises:
            ValueError: Если попытка кражи провалилась
        """
        goose = self.index_dict_goose.search_goose(goose_name)
        player = self.index_dict_player.search_player(player_name)
        if not isinstance(goose, WarGoose):
            raise TypeError
        result_stealing = goose.steal_chip()
        if result_stealing:
            random_chip_index = random.randint(0, len(self.chip_collection) - 1)
            random_chip = self.chip_collection[random_chip_index]
            if not isinstance(random_chip, Chip):
                raise TypeError()
            stolen_value = random_chip.value
            player.balance -= stolen_value
            goose.balance += stolen_value
            return random_chip
        else:
            raise ValueError('Гусь потерял равновесие и не смог украсть фишку')

    def honk_goose_honk(self, goose_name: str, player_name: str) -> int:
        """
        Гогочущий гусь пытается напугать игрока громким криком.

        Args:
            goose_name: Имя гогочущего гуся
            player_name: Имя игрока-жертвы

        Returns:
            Украденная сумма

        Raises:
            ValueError: Если попытка провалилась
        """
        goose = self.index_dict_goose.search_goose(goose_name)
        player = self.index_dict_player.search_player(player_name)
        if not isinstance(goose, HonkGoose):
            raise TypeError()
        result_honking = goose.honk()
        if result_honking:
            stolen_value = goose.honk_volume
            player.balance -= stolen_value
            goose.balance += stolen_value
            return stolen_value
        else:
            raise ValueError('Гусь потерял равновесие и крикнул не в ту сторону')

    def recreate_goose(self, del_goose: Goose, new_goose: Goose) -> None:
        """
        Замена одного гуся на другого.

        Args:
            del_goose: Гусь для удаления
            new_goose: Новый гусь для добавления
        """
        index = self.goose_collection.items.index(del_goose)
        self.goose_collection.pop(index)
        self.index_dict_goose.pop(del_goose)
        self.add_goose(new_goose)

    def player_bet(self, player_name: str, bet_value: int, bet_type: int | str) -> bool:
        """
        Размещение ставки игрока в рулетку.

        Args:
            player_name: Имя игрока
            bet_value: Размер ставки
            bet_type: Тип ставки (число 0-36 или строка типа 'чётное', 'красное')

        Returns:
            True если выигрыш, False если проигрыш

        Raises:
            ValueError: Если баланс недостаточен,
                номер некорректен или тип ставки неверен
        """
        player = self.index_dict_player.search_player(player_name)
        if player.balance < bet_value:
            raise ValueError('Ставка больше чем баланс игрока')
        player.balance -= bet_value
        if isinstance(bet_type, int):
            if -1 < bet_type < 37:
                if bet_type == random.randint(0, 36):
                    player.balance += 35 * bet_value
                    return True
                return False
            else:
                raise ValueError('Нужно выбрать число от 0 до 36')
        if isinstance(bet_type, str):
            if bet_type in (
                'чёрное',
                'черное',
                'красное',
                'чётное',
                'четное',
                'нечётное',
                'нечетное',
            ):
                if random.randint(0, 36) % 2:
                    player.balance += bet_value * 2
                    return True
                return False
            else:
                raise ValueError('Сделайте корректную ставку')
