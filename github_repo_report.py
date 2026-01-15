import requests
import csv
from datetime import datetime

REPOS = [
    "python/cpython",
    "kubernetes/kubernetes",
    "docker/docker-py"
]

OUTPUT_FILE = "github_repo_report.csv"
GITHUB_API_URL = "https://api.github.com/repos/"


def fetch_repo_data(repo):
    response = requests.get(GITHUB_API_URL + repo)
    response.raise_for_status()
    data = response.json()

    return {
        "repository": repo,
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "open_issues": data["open_issues_count"],
        "last_updated": data["updated_at"]
    }


def generate_report():
    results = []
    for repo in REPOS:
        try:
            results.append(fetch_repo_data(repo))
            print(f"Fetched data for {repo}")
        except Exception as e:
            print(f"Failed to fetch {repo}: {e}")

    with open(OUTPUT_FILE, "w", newline="") as csvfile:
        fieldnames = ["repository", "stars", "forks", "open_issues", "last_updated"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"\n✅ Report generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_report()

