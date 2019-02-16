"""File a github issue."""
from urllib import request


def get_github_issues():
    """Get the issues for this project."""
    url = 'https://api.github.com/repos/pocc/apigen/issues'
    result = request.Request(url=url)
    print(result)


def file_new_github_issue(title, body, labels):
    """File a github issue using the API."""
    post_dict = {
      "title": title,
      "body": body,
      "assignee": "pocc",
      "labels": labels
    }
    url = 'https://api.github.com/repos/pocc/apigen/issues'
    request.Request(url=url, data=post_dict)

get_github_issues()