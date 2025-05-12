import csv
import sys
import requests
from datetime import datetime
import webbrowser

GITHUB_API_URL = "https://api.github.com"

ORG_NAME = "clean-code-craft-p-1"
ACCESS_TOKEN = ""
SINCE_DATE = ""


def get_repos_updated_since(org_name, since_date):
    url = f"{GITHUB_API_URL}/orgs/{org_name}/repos"
    headers = {"Authorization": f"token {ACCESS_TOKEN}"}
    params = {"since": since_date, "per_page": 100}
    repos = []

    while url:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        repos.extend(response.json())
        url = response.links.get("next", {}).get("url")

    return repos


def get_repo_details(repo_name):
    headers = {"Authorization": f"token {ACCESS_TOKEN}"}
    branches_url = f"{GITHUB_API_URL}/repos/{ORG_NAME}/{repo_name}/branches"
    pulls_url = f"{GITHUB_API_URL}/repos/{ORG_NAME}/{repo_name}/pulls"

    # Get number of branches
    branches_response = requests.get(branches_url, headers=headers)
    branches_response.raise_for_status()
    num_branches = len(branches_response.json())

    # Get latest pull request
    pulls_response = requests.get(pulls_url, headers=headers, params={"state": "all", "sort": "updated", "direction": "desc"})
    pulls_response.raise_for_status()
    pulls = pulls_response.json()
    if pulls:
        latest_pr = pulls[0]
        pr_url = latest_pr["url"]
        pr_files_link = latest_pr["html_url"] + '/files'
        pr_response = requests.get(pr_url, headers=headers)
        pr_response.raise_for_status()
        pr_details = pr_response.json()
        pr_lines_changed = pr_details["additions"] + pr_details["deletions"]
    else:
        pr_files_link = None
        pr_lines_changed = 0

    return num_branches, pr_files_link, pr_lines_changed


def main():
    repos = get_repos_updated_since(ORG_NAME, SINCE_DATE)
    output_data = []

    for repo in repos:
        repo_name = repo["name"]
        updated_at = repo["updated_at"]

        if datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ") >= datetime.strptime(SINCE_DATE, "%Y-%m-%dT%H:%M:%SZ"):
            print(f"Processing repository: {repo_name} ", end='')
            num_branches, pr_link, pr_lines_changed = get_repo_details(repo_name)
            output_data.append([repo_name, num_branches, pr_lines_changed, pr_link])
            if pr_lines_changed > 0 or num_branches > 2:
                webbrowser.open(pr_link)
                print(f' - launched')
            else:
                print(f' - no changes')
        else:
            print(f"Skipping repository: {repo_name} (updated on {updated_at})")

    with open("repos_report.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Repository", "Branches", "Lines Changed", "Latest PR Link"])
        writer.writerows(output_data)


if __name__ == "__main__":
    ACCESS_TOKEN = sys.argv[1]
    SINCE_DATE = sys.argv[2]
    main()