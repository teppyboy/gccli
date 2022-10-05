import requests

class GitHub:
    """
    A quick wrapper for GitHub API
    """
    def __init__(self, **kwargs):
        if kwargs.get("gh_user")
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': 'token ' + self.token,
            'Accept': 'application/vnd.github.v3+json'
        })

    def get(self, url, params=None):
        """
        GET request
        """
        return self.session.get(url, params=params)

    def post(self, url, data=None):
        """
        POST request
        """
        return self.session.post(url, data=data)

    def patch(self, url, data=None):
        """
        PATCH request
        """
        return self.session.patch(url, data=data)

    def delete(self, url, data=None):
        """
        DELETE request
        """
        return self.session.delete(url, data=data)

    def get_repos(self, org):
        """
        Get all repos for an organization
        """
        url = 'https://api.github.com/orgs/{}/repos'.format(org)
        return self.get(url)

    def get_repo(self, org, repo):
        """
        Get a repo
        """
        url = 'https://api.github.com/repos/{}/{}/'.format(org, repo)
        return self.get(url)

    def get_repo_branches(self, org, repo):
        """
        Get all branches for a repo
        """
        url = 'https://api.github.com/repos/{}/{}/branches'.format(org, repo)
        return self.get(url)

    def get_repo_branch(self, org, repo, branch):
        """
        Get a branch for a repo
        """
        url = 'https://api.github.com/repos/{}/{}/branches/{}'.format(org, repo, branch)
        return self.get(url)

    def get_repo_branch_protection(self, org, repo, branch):
        """
        Get branch protection for a repo
        """
        url = 'https://api.github.com/repos/{}/{}/branches/{}/protection'.format(org, repo, branch)
        return self.get(url)

    def get_repo_branch_protection_required_status_checks(self, org, repo, branch):
        """
        Get branch protection required status checks for a repo
        """
        url = 'https://api.github.com/repos/{}/{}/branches/{}/protection/required_status_checks'.format(org, repo, branch)
        return self.get(url)
