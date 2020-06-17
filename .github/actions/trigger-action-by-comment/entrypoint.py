import os
import re

import requests


def get_action_input(name):
    return os.getenv(f"INPUT_{name.upper()}")


def get_job_from_comment(comment):
    return re.search(r"trigger (.+)", comment).group(1)


def main():
    token = get_action_input("token")
    pull_num = get_action_input("pull_number")
    comment = get_action_input("comment")
    job = get_job_from_comment(comment)

    base_url = "https://api.github.com/repos/harupy/trigger-action-by-comment"
    headers = {
        "Accept": "application/vnd.github.antiope-preview+json",
        "authorization": "Bearer {}".format(token),
    }

    pr = requests.get(base_url + f"/pulls/{pull_num}")
    pr_sha = pr.json()["head"]["sha"]
    suites = requests.get(
        base_url + "/commits/" + pr_sha + "/check-suites", headers=headers,
    )

    # filter check-suites by job
    filtered = []
    for suite in suites.json()["check_suites"]:
        check_runs = requests.get(
            base_url + f"/check-suites/{suite['id']}/check-runs", headers=headers,
        )
        if any(cr["name"] == job for cr in check_runs.json()["check_runs"]):
            filtered.append(suite)

    # re-run filtered check-suites
    for suite in filtered:
        res = requests.get(base_url + f"/{suite['id']}/check-suites", headers=headers,)
        print(res.status_code)


if __name__ == "__main__":
    main()
