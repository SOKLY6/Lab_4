from adapter import casino_simulation
import questionary


def input_args() -> tuple[int, int | None]:
    steps = questionary.text(
        'Введите количество шагов симуляции: ',
        validate=lambda text: text.isdigit(),
    ).ask()
    seed = questionary.text(
        'Если хотите, можете ввести сид для генерации команд\n'
        'в ином случае нажмите enter: ',
        validate=lambda text: text.isdigit() or text == "",
    ).ask()

    if seed == '':
        seed = None
    else:
        seed = int(seed)
    return int(steps), seed


def cli():
    steps, seed = input_args()
    casino_simulation.run_simulation_casino(steps, seed)
