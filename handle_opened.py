import json
import re
from jira_connection import jira
from Github import github

with open('config.json') as config:
  config_dict = json.load(config)

project_regex = re.compile('%s-[0-9]+' %(config_dict['jira']['projectKey']))

def handle_opened(body):
  pr_title = body['pull_request']['title']
  pr_id = body['pull_request']['number']
  print('PR %s has been opened' %(pr_title))
  test = project_regex.search(pr_title)
  if test:
    gh = github(config['github_token'])
    ticket = test.group(0)
    print('should act on ticket %s' %(ticket))
    jira_ticket = jira.issue(ticket)
    transitions = config_dict['action_mapping']['opened']
    usable_transition = None
    for transition in transitions:
      if transition['match']:
        repo = gh.get_repo(config_dict['github_repo'])
        matching_prs = [pr['number'] for pr in repo.search_issues('is:pr %s' %(transition['match']))]
