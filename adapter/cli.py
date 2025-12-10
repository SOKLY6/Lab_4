from adapter import casino_simulation


def input_args() -> tuple[int, int | None]:
    steps = int(input('Введите количество действий для симуляции: '))
    seed = input(
        'Если хотите, можете ввести сид для генерации команд\n'
        'в ином случае нажмите enter: '
    )
    if seed == '':
        seed = None
    else:
        seed = int(seed)
    return steps, seed


def cli():
    steps, seed = input_args()
    casino_simulation.run_simulation_casino(steps, seed)
