import collections
import json
import pprint

from ..facades import github_facade
import settings

DISPLAY = '{}\n\n'


ISSUE_ATTRIBUTES = [
    'url', 'repository_url', 'labels_url', 'comments_url',
    'events_url', 'html_url', 'id', 'number', 'title', 'user',
    'labels', 'state', 'locked', 'assignee', 'assignees', 'milestone',
    'comments', 'created_at', 'updated_at', 'closed_at', 'body', 'score',
    'pull_request', 'author_association'
]

Issue = collections.namedtuple('Issue', ISSUE_ATTRIBUTES)


def create_test_fixture(fixture_filename, issues):
    """
    Write a file with the given issue information to be used for testing

    @param str fixture_filename: Name of the file to be created
    @param issues: Response of issue request
    """
    if fixture_filename:
        fixtures_file_path = settings.PROJECT_ROOT + '/tests/fixtures/' + fixture_filename + '.txt'
        with open(fixtures_file_path, 'w') as f:
            pretty_json = pprint.pprint(json.dumps(issues))
            f.write(pretty_json)

def get_search_issues(fixture_filename, **search):
    """
    Fetch issues given search key, value pairs
    """
    issues = json.loads(github_facade.fetch_search_issues(**search).text)
    create_test_fixture(fixture_filename, issues)

    items = issues.get('items')
    if not items:
        return

    results = []

    for attrs in items:
        # set all fields to None to allow for defaults
        Issue.__new__.__defaults__ = (None,) * len(Issue._fields)
        results.append(Issue(**attrs))

    return results

def issues_attr(issues, attr_name):
    """
    Helper method to access a given attribute for an iterable of Issue's

    @param list[Issue] issues: List instances to access
    @param str attr_name: Attribute that exists on each List item

    @return: Value of attribute from each List
    @rtype: list
    """
    results = []
    if not issues:
        return

    for issue in issues:
        value = getattr(issue, attr_name)
        if value:
            results.append(value)
    return results

def display_issues(milestone_id):
    issues = get_issues(milestone_id)
    return ''.join([DISPLAY.format(issue.body) for issue in issues.get("results")])

def search_issues(count=False, **search):
    issues = get_search_issues(**search)
    issues_display = ''.join([DISPLAY.format(issue.body) for issue in issues['results']])

    if count:
        issues_display += "Count: %s" % issues.get('count')

    return issues_display
