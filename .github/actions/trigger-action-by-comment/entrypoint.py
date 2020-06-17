import os
import re

import requests


def get_action_input(name):
    return os.getenv(f"INPUT_{name.upper()}")


def parse_job(comment):
    return re.search(r"trigger (.+)").group(1)


def main():
    pull_num = get_action_input("pull_number")
    comment = get_action_input("comment")
    job = parse_job(comment)
    print(pull_num, comment, job)


if __name__ == "__main__":
    main()
