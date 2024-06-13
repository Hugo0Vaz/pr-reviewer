#                                   _
#    _ __  _ __      _ __ _____   _(_) _____      _____ _ __
#   | '_ \| '__|____| '__/ _ \ \ / / |/ _ \ \ /\ / / _ \ '__|
#   | |_) | | |_____| | |  __/\ V /| |  __/\ V  V /  __/ |
#   | .__/|_|       |_|  \___| \_/ |_|\___| \_/\_/ \___|_|
#   |_|
#
#   A Pull Request Review Script
#

import typer
import requests
import base64

from typer.params import Option
from typing_extensions import Annotated


def string_to_base64(s):
    return base64.b64encode(s.encode('utf-8'))


def base64_to_string(b):
    return base64.b64decode(b).decode('utf-8')


def get_file_content(url: str, gh_token: str) -> str:
    """ get the file content """

    headers = {
        'Authorization': f'token {gh_token}',
        'Accept': 'application/vnd.github+json',
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(
            f"Error fetching file contents: {response.status_code}")

    return base64_to_string(response.json()['content'])


def get_pr_file_list(pr_number: str, repo_ownr: str, repo_name: str, gh_token: str):
    """ get list of files and chuncks """

    file_list = []

    url = f'https://api.github.com/repos/{repo_ownr}/{repo_name}/pulls/{pr_number}/files'
    headers = {
        'Authorization': f'token {gh_token}',
        'Accept': 'application/vnd.github+json',
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error fetching pull request: {response.status_code}")

    for file in response.json():
        print(file['filename'])
        file_list.append(
            (
                file['filename'],
                file['patch'],
                get_file_content(file['contents_url'], gh_token)
            )
        )

    return file_list


def get_pr_data(pr_number: str, repo_ownr: str, repo_name: str, gh_token: str) -> requests.Response:
    """ gets the pull request title """

    url = f'https://api.github.com/repos/{repo_ownr}/{repo_name}/pulls/{pr_number}'
    headers = {
        'Authorization': f'token {gh_token}',
        'Accept': 'application/vnd.github+json',
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error fetching pull request: {response.status_code}")
    return response


def printout(fstring: str, mode: bool):
    """ prints out if set to verbose """
    if mode:
        print(fstring)


def print_script_signature(pr_number, repo_ownr, repo_name, verbose):
    """ prints the program signature """

    signature = f'\nRunning reviews on PR #{pr_number} in {repo_ownr}/{repo_name}...\n'

    len_signature = len(signature) - 2

    for _ in range(len_signature):
        signature += '='

    signature = signature + '\n'

    printout(signature, verbose)


def main(
    pr_number: int,
    repo_ownr: str,
    repo_name: str,
    gh_token:  str,

    review_title: Annotated[bool, typer.Option(
        help="Option to review the PR title")] = True,
    review_body: Annotated[bool, typer.Option(
        help="Option to review the PR body")] = True,
    review_diffs: Annotated[bool, typer.Option(
        help="Option to review the PR diffs")] = True,
    debug: Annotated[bool, typer.Option(
        help="Option to enable debug mode")] = False,
    verbose: Annotated[bool, typer.Option(
        help="Option to enable verbose mode")] = False,

    max_files: int = Option(
        30, help="Option to set the max number of files reviewed")
):

    print_script_signature(pr_number, repo_ownr, repo_name, verbose)

    pr_title: str
    pr_body: str

    if review_title or review_body:
        pr_data = get_pr_data(str(pr_number), repo_ownr,
                              repo_name, gh_token).json()
        pr_title = pr_data['title']
        pr_body = pr_data['body']

        if review_title != False:
            printout("Reviewing the title:", verbose)
            # TODO: implement title review code
            printout(f'\t{pr_title}', verbose)

        if review_body != False:
            printout("Reviewing the body:", verbose)
            # TODO: implement body review code
            printout(f'\t{pr_body}', verbose)

    if review_diffs != False:
        printout("Reviewing the files:", verbose)
        printout(f'\tThe max_files is set to: {max_files}', verbose)

        changed_files = get_pr_file_list(
            str(pr_number), repo_ownr, repo_name, gh_token)

        for file in changed_files:
            # print()


if __name__ == '__main__':
    typer.run(main)
