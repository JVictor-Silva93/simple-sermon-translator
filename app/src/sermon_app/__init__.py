import argparse


def hello() -> str:
    return "Hello from app!"

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="sermon-app",
        description="Runs the user front facing app.",
    )
    parser.parse_args()
    print(hello())
