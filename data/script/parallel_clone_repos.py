import os
import subprocess
from multiprocessing import Pool
from github import Github

ORG = "huggingface"
MIRROR_DIRECTORY = "hf_public_repos"


def get_repos(username, access_token=None, include_fork=False):
    """Fetches repositories for a particular GitHub user."""
    g = Github(access_token)
    user = g.get_user(username)

    results = []
    for repo in user.get_repos():
        if repo.fork is False:
            results.append(repo.name)
        else:
            if include_fork is True:
                results.append(repo.name)

    return results


def mirror_repository(repository, force=False):
    """Locally clones a repository."""
    repository_url = f"https://github.com/{ORG}/{repository}.git"
    repository_path = os.path.join(MIRROR_DIRECTORY, repository)
    if os.path.exists(repository_path) and not force:
        print(f"exit, skip: {repository}")
        return
    # Clone the repository
    result = subprocess.run(
        ["git", "clone", repository_url, repository_path,
         '--config', 'http.proxy=http://127.0.0.1:7890',
         '--config', 'https.proxy=http://127.0.0.1:7890']
    )
    if result.returncode != 0 and not force:
        print(f"retry:{repository}")
        mirror_repository(repository, True)


def run():
    # Create the mirror directory if it doesn't exist
    if not os.path.exists(MIRROR_DIRECTORY):
        os.makedirs(MIRROR_DIRECTORY)

    # Get the list of repositories in the organization
    if not os.environ["GH_ACCESS_TOKEN"]:
        raise ValueError("You must set `GH_ACCESS_TOKEN` as an env variable.")
    repositories = get_repos(ORG, os.environ["GH_ACCESS_TOKEN"])
    print(f"Total repositories found: {len(repositories)}.")

    # Mirror repositories using multiprocessing
    print("Cloning repositories.")
    with Pool() as pool:
        pool.map(mirror_repository, repositories)


if __name__ == "__main__":
    if os.environ.get("MIRROR_DIRECTORY"):
        MIRROR_DIRECTORY = os.environ.get("MIRROR_DIRECTORY")
    if os.environ.get("ORG"):
        ORG = os.environ.get("ORG")
    run()
