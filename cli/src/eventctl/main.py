import argparse


def main() -> int:
    parser = argparse.ArgumentParser(prog="eventctl", description="eventd control CLI")
    parser.add_argument("--version", action="store_true", help="Show version")
    args = parser.parse_args()

    if args.version:
        print("eventctl 0.1.0")
    else:
        print("eventctl is ready")
    return 0
