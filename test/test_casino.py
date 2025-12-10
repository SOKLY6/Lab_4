import pytest
from domain.casino_entities import Chip, Player, WarGoose, HonkGoose
from usecases.casino import Casino
from repository.casino_collections import (
    ChipCollection,
    PlayerCollection,
    GooseCollection,
    IndexDictChip,
    IndexDictPlayer,
    IndexDictGoose
)


@pytest.fixture
def casino():
    """Фикстура для создания пустого казино"""
    return Casino(
        ChipCollection(),
        PlayerCollection(),
        GooseCollection(),
        IndexDictChip(),
        IndexDictPlayer(),
        IndexDictGoose()
    )


@pytest.fixture
def casino_with_players(casino):
    """Фикстура казино с игроками"""
    player1 = Player("Игрок1", 1000)
    player2 = Player("Игрок2", 2000)
    player3 = Player("Игрок3", 3000)
    casino.add_player(player1)
    casino.add_player(player2)
    casino.add_player(player3)
    return casino


@pytest.fixture
def casino_with_geese(casino):
    """Фикстура казино с гусями"""
    goose1 = WarGoose("Гусь1", 40)
    goose2 = HonkGoose("Гусь2", 30)
    casino.add_goose(goose1)
    casino.add_goose(goose2)
    return casino



def test_create_player():
    """Тест создания игрока"""
    player = Player("Николай Сергеевич", 1000)
    assert player.name == "Николай Сергеевич"
    assert player.balance == 1000


def test_create_war_goose():
    """Тест создания боевого гуся"""
    goose = WarGoose("Голеадор", 50)
    assert goose.name == "Голеадор"
    assert goose.honk_volume == 50
    assert goose.balance == 0


def test_create_honk_goose():
    """Тест создания гогочущего гуся"""
    goose = HonkGoose("Мирон", 30)
    assert goose.name == "Мирон"
    assert goose.honk_volume == 30
    assert goose.balance == 0


def test_create_chip():
    """Тест создания фишки"""
    chip = Chip("red", 25)
    assert chip.colour == "red"
    assert chip.value == 25


def test_chip_add():
    """Тест метода __add__ для фишки"""
    chip = Chip("blue", 10)
    chip += 5
    assert chip.value == 15


def test_add_player_and_len(casino):
    """Тест добавления игроков"""
    player1 = Player("Игрок1", 1000)
    
    casino.add_player(player1)
    assert len(casino.player_collection) == 1


def test_add_goose(casino):
    """Тест добавления гусей"""
    goose1 = WarGoose("Гусь1", 40)
    
    casino.add_goose(goose1)
    assert len(casino.goose_collection) == 1


def test_add_chip(casino):
    """Тест добавления фишек"""
    chip = Chip("purple", 100)
    casino.add_chip(chip)
    assert len(casino.chip_collection) == 6


def test_get_player_slice(casino_with_players):
    """Тест получения игрока по индексу"""
    assert casino_with_players.get_player_slice(0).name == "Игрок1"
    assert casino_with_players.get_player_slice(1).name == "Игрок2"
    assert casino_with_players.get_player_slice(-1).name == "Игрок3"


def test_get_player_slice_range(casino_with_players):
    """Тест получения среза игроков"""
    result = casino_with_players.get_player_slice(slice(0, 2))
    assert len(result) == 2
    assert result[0].name == "Игрок1"
    assert result[1].name == "Игрок2"


def test_get_goose_slice(casino_with_geese):
    """Тест получения гуся по индексу"""
    assert casino_with_geese.get_goose_slice(0).name == "Гусь1"
    assert casino_with_geese.get_goose_slice(1).name == "Гусь2"


def test_get_chip_slice(casino):
    """Тест получения фишки по индексу"""
    first_chip = casino.get_chip_slice(0)
    assert isinstance(first_chip, Chip)


def test_iter_player(casino_with_players):
    """Тест итерации по игрокам"""
    players = list(casino_with_players.iter_player())
    assert len(players) == 3
    assert players[0].name == "Игрок1"


def test_iter_goose(casino_with_geese):
    """Тест итерации по гусям"""
    geese = list(casino_with_geese.iter_goose())
    assert len(geese) == 2


def test_iter_chip(casino):
    """Тест итерации по фишкам"""
    chips = list(casino.iter_chip())
    assert len(chips) == 5
    assert all(isinstance(chip, Chip) for chip in chips)


def test_pop_player(casino_with_players):
    """Тест удаления игрока"""
    deleted_player = casino_with_players.pop_player(2)
    assert deleted_player.name == "Игрок2"
    assert len(casino_with_players.player_collection) == 2


def test_pop_goose(casino_with_geese):
    """Тест удаления гуся"""
    deleted_goose = casino_with_geese.pop_goose(1)
    assert deleted_goose.name == "Гусь1"
    assert len(casino_with_geese.goose_collection) == 1


def test_pop_chip(casino):
    """Тест удаления фишки"""
    deleted_chip = casino.pop_chip(1)
    assert isinstance(deleted_chip, Chip)
    assert len(casino.chip_collection) == 4


def test_search_player(casino):
    """Тест поиска игрока по имени"""
    player = Player("Николай Сергеевич", 1000)
    casino.add_player(player)
    
    found_player = casino.search_player("Николай Сергеевич")
    assert found_player.name == "Николай Сергеевич"


def test_search_player_not_found(casino):
    """Тест поиска несуществующего игрока"""
    with pytest.raises(ValueError):
        casino.search_player("Николай Сергеевич")


def test_search_player_balance(casino):
    """Тест поиска баланса игрока"""
    player = Player("Николай Сергеевич", 5000)
    casino.add_player(player)
    balance = casino.search_player_balance("Николай Сергеевич")
    assert balance == 5000


def test_search_goose(casino):
    """Тест поиска гуся по имени"""
    goose = WarGoose("Голеадор", 50)
    casino.add_goose(goose)
    
    found_goose = casino.search_goose("Голеадор")
    assert found_goose.name == "Голеадор"


def test_search_goose_not_found(casino):
    """Тест поиска несуществующего гуся"""
    with pytest.raises(ValueError):
        casino.search_goose("Не Голеадор")


def test_search_goose_balance(casino):
    """Тест поиска баланса гуся"""
    goose = WarGoose("Голеадор", 50)
    casino.add_goose(goose)
    balance = casino.search_goose_balance("Голеадор")
    assert balance == 0


def test_search_goose_honk_volume(casino):
    """Тест поиска громкости гуся"""
    goose = HonkGoose("Мирон", 75)
    casino.add_goose(goose)
    volume = casino.search_goose_honk_volume("Мирон")
    assert volume == 75


def test_search_chip_value(casino):
    """Тест поиска стоимости фишки по цвету"""
    value = casino.search_chip_value("red")
    assert value == 25


def test_search_chip_value_not_found(casino):
    """Тест поиска несуществующей фишки"""
    with pytest.raises(IndexError):
        casino.search_chip_value("purple")


def test_player_bet_insufficient_balance(casino):
    """Тест ставки при недостаточном балансе"""
    player = Player("Николай Сергеевич", 100)
    casino.add_player(player)
    
    with pytest.raises(ValueError, match="Ставка больше чем баланс игрока"):
        casino.player_bet("Николай Сергеевич", 500, 5)


def test_player_bet_invalid_number(casino):
    """Тест ставки с невалидным числом"""
    player = Player("Николай Сергеевич", 1000)
    casino.add_player(player)
    
    with pytest.raises(ValueError, match="Нужно выбрать число от 0 до 36"):
        casino.player_bet("Николай Сергеевич", 100, 50)


def test_player_bet_invalid_string(casino):
    """Тест ставки с невалидной строкой"""
    player = Player("Николай Сергеевич", 1000)
    casino.add_player(player)
    
    with pytest.raises(ValueError, match="Сделайте корректную ставку"):
        casino.player_bet("Николай Сергеевич", 100, "синее")


def test_player_bet_win_number(casino, mocker):
    """Тест выигрышной ставки на число"""
    player = Player("Счастливый Николай Сергеевич", 1000)
    casino.add_player(player)
    
    mocker.patch('random.randint', return_value=7)
    
    result = casino.player_bet("Счастливый Николай Сергеевич", 100, 7)
    assert result is True
    assert player.balance == 1000 - 100 + 35 * 100


def test_player_bet_lose_number(casino, mocker):
    """Тест проигрышной ставки на число"""
    player = Player("Грустный Николай Сергеевич", 1000)
    casino.add_player(player)
    
    mocker.patch('random.randint', return_value=7)
    
    result = casino.player_bet("Грустный Николай Сергеевич", 100, 5)
    assert result is False
    assert player.balance == 900


def test_player_bet_win_string(casino, mocker):
    """Тест выигрышной ставки на чётное/нечётное"""
    player = Player("Счастливый Николай Сергеевич", 1000)
    casino.add_player(player)
    
    mocker.patch('random.randint', return_value=1)
    
    result = casino.player_bet("Счастливый Николай Сергеевич", 100, "нечётное")
    assert result is True
    assert player.balance == 1000 - 100 + 100 * 2


def test_player_bet_lose_string(casino, mocker):
    """Тест проигрышной ставки на чётное/нечётное"""
    player = Player("Грустный Николай Сергеевич", 1000)
    casino.add_player(player)
    
    mocker.patch('random.randint', return_value=0)
    
    result = casino.player_bet("Грустный Николай Сергеевич", 100, "нечётное")
    assert result is False
    assert player.balance == 900


def test_war_goose_steal_chip_success(casino, mocker):
    """Тест успешной кражи фишки боевым гусём"""
    player = Player("Жертва", 1000)
    goose = WarGoose("Вор", 50)
    
    casino.add_player(player)
    casino.add_goose(goose)
    
    mocker.patch.object(goose, 'steal_chip', return_value=100)
    mocker.patch('random.randint', return_value=0)
    
    initial_balance = player.balance
    stolen_chip = casino.war_goose_steal_chip("Вор", "Жертва")
    
    assert isinstance(stolen_chip, Chip)
    assert player.balance < initial_balance
    assert goose.balance > 0


def test_war_goose_steal_chip_failed(casino, mocker):
    """Тест неудачной кражи фишки боевым гусём"""
    player = Player("Жертва", 1000)
    goose = WarGoose("Неудачник", 50)
    
    casino.add_player(player)
    casino.add_goose(goose)
    
    mocker.patch.object(goose, 'steal_chip', return_value=0)
    
    with pytest.raises(ValueError, match="Гусь потерял равновесие и не смог украсть фишку"):
        casino.war_goose_steal_chip("Неудачник", "Жертва")


def test_honk_goose_honk_success(casino, mocker):
    """Тест успешного гоготания гуся"""
    player = Player("Жертва", 1000)
    goose = HonkGoose("Гоготун", 75)
    
    casino.add_player(player)
    casino.add_goose(goose)
    
    mocker.patch.object(goose, 'honk', return_value=75)
    
    initial_balance = player.balance
    stolen_value = casino.honk_goose_honk("Гоготун", "Жертва")
    
    assert stolen_value == 75
    assert player.balance == initial_balance - 75
    assert goose.balance == 75


def test_honk_goose_honk_failed(casino, mocker):
    """Тест неудачного гоготания гуся"""
    player = Player("Жертва", 1000)
    goose = HonkGoose("Тихоня", 30)
    
    casino.add_player(player)
    casino.add_goose(goose)
    
    mocker.patch.object(goose, 'honk', return_value=0)
    
    with pytest.raises(ValueError, match="Гусь потерял равновесие и крикнул не в ту сторону"):
        casino.honk_goose_honk("Тихоня", "Жертва")


def test_recreate_goose(casino):
    """Тест пересоздания гуся"""
    old_goose = WarGoose("Старый", 30)
    new_goose = HonkGoose("Новый", 50)
    
    casino.add_goose(old_goose)
    assert len(casino.goose_collection) == 1
    
    casino.recreate_goose(old_goose, new_goose)
    
    assert len(casino.goose_collection) == 1
    found_goose = casino.search_goose("Новый")
    assert found_goose.name == "Новый"
    assert isinstance(found_goose, HonkGoose)
