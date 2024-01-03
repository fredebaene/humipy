import argparse
from humipy.cli import render_app


def get_command_line_arguments() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = get_command_line_arguments()
    render_app(args.dev)


if __name__ == "__main__":
    main()