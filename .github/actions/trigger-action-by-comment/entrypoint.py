import os
import re

import requests


def get_action_input(name):
    return os.getenv(f"INPUT_{name.upper()}")


def parse_job(comment):
    return re.search(r"trigger (.+)", comment).group(1)


def filter_check_suites_by_job(suites, job):
    filtered = []
    for suite in suites:
        res = requests.get(base_url + f"/check-suites/{suites['id']}/check-runs")
        if any(cr["name"] == job for cr in res.json()["check_runs"]):
            filtered.append(suite)
    return filtered


def main():
    TOKEN = get_action_input('token')
    pull_num = get_action_input("pull_number")
    comment = get_action_input("comment")
    job = parse_job(comment)

    headers = {
        "Accept": "application/vnd.github.antiope-preview+json",
        "authorization": "Bearer {}".format(TOKEN),
    }

    base_url = "https://api.github.com/repos/harupy/trigger-action-by-comment"

    pr = requests.get(base_url + f"pulls/{pull_num}")
    pr_sha = pr.json()["head"]["sha"]

    suites = requests.get(
        base_url + "/commits/" + pr_sha + "/check-suites", headers=suites_headers,
    )
    suites = suites.json()["check_suites"]
    suites = filter_check_suites_by_job(suites, job)

    print(suites)


if __name__ == "__main__":
    main()
