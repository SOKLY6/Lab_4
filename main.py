from adapter.cli import cli


def main() -> None:
    try:
        cli()
    except Exception as e:
        print(f'{e}')


if __name__ == '__main__':
    main()
