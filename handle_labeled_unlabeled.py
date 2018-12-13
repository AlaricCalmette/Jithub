import json
import re
from jira_connection import jira_link

with open('config.json') as config:
  config_dict = json.load(config)

project_regex = re.compile('%s-[0-9]+' %(config_dict['jira']['projectKey']))

def handle_labeled_unlabeled(body):
  added_or_removed = 'added' if body['action'] == 'labeled' else 'removed'
  print('label %s %s to pr %s' %(body['label']['name'], added_or_removed, body['pull_request']['title']))
  test = project_regex.search(body['pull_request']['title'])

  if test:
    ticket = test.group(0)
    print('Should act on jira ticket %s' %(ticket))
    jira_ticket = jira_link.issue(ticket)

    try:
      transition = config_dict['action_mapping'][body['action']][body['label']['name']]
      transitionName = transition['name']
    except KeyError:
      raise Exception('No config matching label %s was found' %(body['label']['name']))

    transitionId = jira_link.find_transitionid_by_name(jira_ticket.id, transitionName)
    if transitionId is not None:
      try:
        jira_ticket.update(transition['fields'])
      except KeyError:
        print('No fields provided for %s' %(transitionName))
      except Exception:
        print('An unknown error occured while trying to update fields of %s' %(ticket))
    else:
      raise Exception('Transition %s does not exist or is not available for %s' %(transitionName, jira_ticket.key))

    jira_link.transition_issue(jira_ticket, transitionId, comment='jithub')
    print('%s has been applied on %s' %(transitionName, jira_ticket.key))
