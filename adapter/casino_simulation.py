import random

import questionary
import typer

from domain.casino_entities import HonkGoose, Player, WarGoose
from repository.casino_collections import (
    ChipCollection,
    GooseCollection,
    IndexDictChip,
    IndexDictGoose,
    IndexDictPlayer,
    PlayerCollection,
)
from usecases.casino import Casino

global casino
casino = Casino(
    ChipCollection(),
    PlayerCollection(),
    GooseCollection(),
    IndexDictChip(),
    IndexDictPlayer(),
    IndexDictGoose(),
)


def setup_casino() -> None:
    """Начальная настройка казино с игроками и гусями"""

    typer.secho('\nСОЗДАНИЕ КАЗИКА:\n', fg=typer.colors.CYAN, bold=True)

    num_players = questionary.select(
        'Сколько игроков хотите создать?', choices=['2', '3', '4', '5']
    ).ask()

    if not num_players:
        raise SyntaxError('Выбор некорректен')

    num_players = int(num_players)

    typer.secho('\nСОЗДАНИЕ ИГРОКОВ:\n', fg=typer.colors.CYAN)
    for i in range(num_players):
        typer.secho(f'Игрок #{i + 1}:', fg=typer.colors.CYAN)

        name = questionary.text('Имя игрока:').ask()
        if not name:
            name = f'Player{i + 1}'

        balance_input = questionary.text(
            'Баланс (от 10 до 100):',
            validate=lambda text: text.isdigit() and 10 <= int(text) <= 100,
        ).ask()

        balance = int(balance_input) if balance_input else 50

        player = Player(name, balance)
        casino.add_player(player)
        typer.secho(
            f"\nИгрок с именем '{name}' создан\nБаланс: {balance}\n",
            fg=typer.colors.BRIGHT_GREEN,
        )

    num_geese = questionary.select(
        'Сколько гусей хотите создать?', choices=['2', '3', '4', '5']
    ).ask()

    if not num_geese:
        raise SyntaxError('Выбор некорректен')

    num_geese = int(num_geese)

    typer.secho('\nСОЗДАНИЕ ГУСЕЙ:\n', fg=typer.colors.CYAN)
    for i in range(num_geese):
        typer.secho(f'Гусь #{i + 1}:', fg=typer.colors.CYAN)

        name = questionary.text('Имя гуся:').ask()
        if not name:
            name = f'Goose{i + 1}'

        goose_type = questionary.select(
            'Тип гуся:', choices=['Боевой (WarGoose)', 'Гогочущий (HonkGoose)']
        ).ask()

        honk_input = questionary.text(
            'Громкость гоготания (от 1 до 10):',
            validate=lambda text: text.isdigit() and 1 <= int(text) <= 10,
        ).ask()

        honk_volume = int(honk_input) if honk_input else 5

        if 'Боевой' in goose_type:
            goose = WarGoose(name, honk_volume)
        else:
            goose = HonkGoose(name, honk_volume)

        casino.add_goose(goose)
        typer.secho(
            f"\nГусь с именем '{name}' создан\nТип: {goose.__class__.__name__}\n"
            f"Громкость: {honk_volume}\n",
            fg=typer.colors.BRIGHT_BLUE,
        )
        typer.echo()

    typer.secho(
        'Казик готов, пора проигрывать деньги(ну или выигрывать XD)!\n',
        fg=typer.colors.CYAN,
        bold=True,
    )


def check_game_over() -> bool:
    """Проверка условий окончания игры"""
    for player in casino.iter_player():
        if player.balance <= 0:
            index = casino.player_collection.items.index(player)
            casino.pop_player(index + 1)
            typer.secho(f"Игрок '{player.name}' стал банкротом", fg=typer.colors.YELLOW)

    if len(casino.player_collection) == 0:
        typer.secho(
            'ГУСИ ПОБЕДИЛИ! ВСЕ ИГРОКИ СТАЛИ БАНКРОТАМИ!',
            fg=typer.colors.BRIGHT_BLUE,
            bold=True,
        )
        return True

    for player in casino.iter_player():
        if player.balance >= 5000:
            typer.secho(
                f"ИГРОКИ ПОБЕДИЛИ! '{player.name}' достиг баланса {player.balance}!",
                fg=typer.colors.BRIGHT_GREEN,
                bold=True,
            )
            return True

    return False


def show_status() -> None:
    """Показывает текущий статус игры"""
    typer.secho('\nСТАТУС ИГРЫ:\n', fg=typer.colors.CYAN)
    typer.secho('Игроки:', fg=typer.colors.BRIGHT_GREEN)
    for i, player in enumerate(casino.iter_player(), 1):
        typer.echo(f'{i}. {player.name}\nБаланс: {player.balance}\n')

    typer.secho('\nГуси:', fg=typer.colors.BRIGHT_BLUE)
    for i, goose in enumerate(casino.iter_goose(), 1):
        goose_type = 'WarGoose' if isinstance(goose, WarGoose) else 'HonkGoose'
        typer.echo(
            f'{i}. {goose_type} {goose.name}\nБаланс: {goose.balance}\n'
            f'Громкость: {goose.honk_volume}\n'
        )
    typer.echo()


def player_bet() -> None:
    """Действие: игрок делает ставку"""
    typer.secho('\nСТАВКА ИГРОКА', fg=typer.colors.YELLOW, bold=True)

    player_choices = []
    for player in casino.iter_player():
        player_choices.append(f'{player.name} (баланс: {player.balance})')

    selected_player = questionary.select(
        'Кто делает ставку?', choices=player_choices
    ).ask()

    if not selected_player:
        raise SyntaxError('Игрок выбран некорректно')

    player_name = selected_player.split(' (')[0]
    player = casino.search_player(player_name)

    bet_value = questionary.text(
        f'Размер ставки (макс. {player.balance}):',
        validate=lambda text: text.isdigit() and 0 < int(text) <= player.balance,
    ).ask()

    if not bet_value:
        raise SyntaxError('Ствака выбрана некорректно')

    bet_value = int(bet_value)

    bet_type_choice = questionary.select(
        'Тип ставки:',
        choices=['Число (0-36)', 'Чётное', 'Нечётное', 'Красное', 'Чёрное'],
    ).ask()

    if not bet_type_choice:
        return

    if 'Число' in bet_type_choice:
        bet_num = questionary.text(
            'На какое число ставите (0-36)?',
            validate=lambda text: text.isdigit() and 0 <= int(text) <= 36,
        ).ask()

        if not bet_num:
            return

        bet_type = int(bet_num)
    else:
        bet_type = str(bet_type_choice).lower()

    try:
        old_balance = player.balance
        result = casino.player_bet(player_name, bet_value, bet_type)

        if result:
            typer.secho(
                f'ВЫИГРЫШ! {player_name}: {old_balance} -> {player.balance}',
                fg=typer.colors.GREEN,
                bold=True,
            )
        else:
            typer.secho(
                f'ПРОИГРЫШ! {player_name}: {old_balance} -> {player.balance}',
                fg=typer.colors.RED,
            )
    except Exception as e:
        typer.secho(f'{e}', fg=typer.colors.RED)


def war_goose_attack() -> None:
    """Действие: боевой гусь атакует игрока"""
    typer.secho('\nАТАКА БОЕВОГО ГУСЯ', fg=typer.colors.YELLOW, bold=True)

    war_geese = [goose for goose in casino.iter_goose() if isinstance(goose, WarGoose)]

    if not war_geese:
        typer.secho('Нет боевых гусей!', fg=typer.colors.YELLOW)
        return

    goose = random.choice(war_geese)
    goose_name = goose.name
    typer.secho(f'Случайно выбран гусь: {goose_name}', fg=typer.colors.YELLOW)

    player = random.choice(casino.iter_player())
    player_name = player.name
    typer.secho(f'Случайно выбран игрок: {player_name}', fg=typer.colors.YELLOW)

    try:
        old_player_balance = player.balance
        old_goose_balance = goose.balance

        stolen_chip = casino.war_goose_steal_chip(goose_name, player_name)

        typer.secho(
            f"Гусь '{goose_name}' украл фишку номиналом {stolen_chip.value}",
            fg=typer.colors.YELLOW,
        )
        typer.secho(
            f'  {player_name}: {old_player_balance} -> {player.balance}',
            fg=typer.colors.YELLOW,
        )
        typer.secho(
            f'  {goose_name}: {old_goose_balance} -> {goose.balance}',
            fg=typer.colors.YELLOW,
        )
    except ValueError as e:
        typer.secho(f'{e}', fg=typer.colors.YELLOW)


def honk_goose_do_honk() -> None:
    """Действие: гогочущий гусь кричит на игрока"""
    typer.secho('\nГОГОТАНИЕ ГУСЯ', fg=typer.colors.YELLOW, bold=True)

    honk_geese = [
        goose for goose in casino.iter_goose() if isinstance(goose, HonkGoose)
    ]

    if not honk_geese:
        typer.secho('Нет гогочущих гусей!', fg=typer.colors.YELLOW)
        return

    goose = random.choice(honk_geese)
    goose_name = goose.name
    typer.secho(f'Случайно выбран гусь: {goose_name}', fg=typer.colors.YELLOW)

    player = random.choice(casino.iter_player())
    player_name = player.name
    typer.secho(f'Случайно выбран игрок: {player_name}', fg=typer.colors.YELLOW)

    try:
        old_player_balance = player.balance
        old_goose_balance = goose.balance

        stolen_value = casino.honk_goose_honk(goose_name, player_name)

        typer.secho(
            f'Гусь {goose_name} напугал {player_name} и украл {stolen_value}!',
            fg=typer.colors.YELLOW,
        )
        typer.secho(
            f"Баланс игрока '{player_name}': {old_player_balance} -> {player.balance}",
            fg=typer.colors.YELLOW,
        )
        typer.secho(
            f"Баланс гуся '{goose_name}': {old_goose_balance} -> {goose.balance}",
            fg=typer.colors.YELLOW,
        )
    except ValueError as e:
        typer.secho(f'{e}', fg=typer.colors.YELLOW)


def recreate_goose() -> None:
    """Действие: пересоздание гуся"""
    typer.secho('\nПЕРЕСОЗДАНИЕ ГУСЯ', fg=typer.colors.YELLOW, bold=True)

    goose_choices = []
    for goose in casino.iter_goose():
        goose_choices.append(
            f'{goose.name} (Тип: {type(goose).__name__}; Баланс: {goose.balance}; '
            f'Сила гоготания: {goose.honk_volume})'
        )

    selected_old = questionary.select(
        'Какого гуся заменить?', choices=goose_choices
    ).ask()

    if not selected_old:
        return

    old_goose_name = selected_old.split(' (')[0]
    old_goose = casino.search_goose(old_goose_name)

    typer.secho('\nСоздание нового гуся', fg=typer.colors.BRIGHT_BLUE)

    name = questionary.text('Имя нового гуся:').ask()
    if not name:
        name = f'Goose{random.randint(100, 10000)}'

    goose_type = questionary.select(
        'Тип гуся:', choices=['Боевой (WarGoose)', 'Гогочущий (HonkGoose)']
    ).ask()

    honk_input = questionary.text(
        'Громкость гоготания (от 1 до 10):',
        validate=lambda text: text.isdigit() and 1 <= int(text) <= 10,
    ).ask()

    honk_volume = int(honk_input) if honk_input else 5

    if 'Боевой' in goose_type:
        new_goose = WarGoose(name, honk_volume)
    else:
        new_goose = HonkGoose(name, honk_volume)

    casino.recreate_goose(old_goose, new_goose)

    typer.secho(f"Гусь '{old_goose_name}' заменен на '{name}'", fg=typer.colors.YELLOW)


def run_simulation_casino(steps: int, seed: int) -> None:
    """Запускает симуляцию казино"""
    if seed is not None:
        random.seed(seed)

    setup_casino()

    commands = {
        1: war_goose_attack,
        2: honk_goose_do_honk,
        3: recreate_goose,
        4: player_bet,
    }

    typer.secho('НАЧАЛО СИМУЛЯЦИИ', fg=typer.colors.CYAN, bold=True)

    show_status()

    for i in range(steps):
        number = random.randint(1, 4)

        command = commands[number]
        command_name = command.__name__
        typer.secho(f'Действие: {command_name}', fg=typer.colors.YELLOW)

        try:
            command()
        except ValueError as e:
            print(f'{e}')
        except IndexError as e:
            print(f'{e}')

        if check_game_over():
            break

        show_status()

        if i < steps - 1:
            input('\nНажмите Enter для следующего шага...')

    typer.secho('СИМУЛЯЦИЯ ЗАВЕРШЕНА', fg=typer.colors.CYAN, bold=True)

    typer.secho('ФИНАЛЬНЫЕ РЕЗУЛЬТАТЫ:', fg=typer.colors.CYAN, bold=True)
    show_status()
