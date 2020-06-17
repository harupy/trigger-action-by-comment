import os

import requests


def get_action_input(name):
    return os.getenv(f"INPUT_{name.upper()}")


def main():
    pull_num = get_action_input("pull_number")
    comment = get_action_input("comment")
    print(pull_num, comment)


if __name__ == "__main__":
    main()
