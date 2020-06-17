import os
import re

import requests


BASE_URL = "https://api.github.com/repos/harupy/trigger-action-by-comment"


def get_action_input(name):
    return os.getenv(f"INPUT_{name.upper()}")


def get_job_from_comment(comment):
    return re.search(r"trigger (.+)", comment).group(1)


def filter_check_suites_by_job(suites, job):
    filtered = []
    for suite in suites:
        check_runs = requests.get(BASE_URL + f"/check-suites/{suite['id']}/check-runs")
        print(check_runs)
        if any(cr["name"] == job for cr in check_runs.json()["check_runs"]):
            filtered.append(suite)
    return filtered


def main():
    TOKEN = get_action_input('token')
    pull_num = get_action_input("pull_number")
    comment = get_action_input("comment")
    job = get_job_from_comment(comment)

    headers = {
        "Accept": "application/vnd.github.antiope-preview+json",
        "authorization": "Bearer {}".format(TOKEN),
    }


    pr = requests.get(BASE_URL + f"/pulls/{pull_num}")
    pr_sha = pr.json()["head"]["sha"]

    suites = requests.get(
        BASE_URL + "/commits/" + pr_sha + "/check-suites", headers=headers,
    )
    suites = suites.json()["check_suites"]
    suites = filter_check_suites_by_job(suites, job)

    print(suites)


if __name__ == "__main__":
    main()
