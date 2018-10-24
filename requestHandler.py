from http.server import BaseHTTPRequestHandler
import json
import re
from jira import JIRA
import traceback
import pdb

with open('config.json') as config:
  config_dict = json.load(config)

project_regex = re.compile('%s-[0-9]+' %(config_dict['jira']['projectKey']))

key_cert_data = None
with open(config_dict['jira']['cert_path']) as key_cert_file:
  key_cert_data = key_cert_file.read()

oauth_dict = {
    'access_token': config_dict['jira']['oauth_token'],
    'access_token_secret': config_dict['jira']['oauth_secret'],
    'consumer_key': config_dict['jira']['consumer_key'],
    'key_cert': key_cert_data
}
jira = JIRA(config_dict['jira']['instance_address'], oauth=oauth_dict)

def handle_labeled_unlabeled(body, action):
  added_or_removed = 'added' if action == 'labeled' else 'removed'
  print('label %s %s to pr %s' %(
  body['label']['name'], added_or_removed, body['pull_request']['title']))
  test = project_regex.search(body['pull_request']['title'])

  if test:
    ticket = test.group(0)
    print('Should act on jira ticket %s' %(ticket))
    jira_ticket = jira.issue(ticket)

    try:
      transition = config_dict['action_mapping'][action][body['label']['name']]
      transitionName = transition['name']
    except KeyError:
      raise Exception('No config matching label %s was found' %(body['label']['name']))

    transitionId = jira.find_transitionid_by_name(jira_ticket.id, transitionName)
    if transitionId is not None:
      try:
        jira_ticket.update(transition['fields'])
      except KeyError:
        print('No fields provided for %s' %(transitionName))
      except Exception:
        print('An unknown error occured while trying to update fields of %s' %(ticket))
    else:
      raise Exception('Transition %s does not exist or is not available for %s' %(transitionName, jira_ticket.key))

    jira.transition_issue(jira_ticket, transitionId, comment='jithub')
    print('%s has been applied on %s' %(transitionName, jira_ticket.key))

def handle_action(body):
  actions = {
    'labeled': handle_labeled_unlabeled,
    'unlabeled': handle_labeled_unlabeled
  }
  try:
    actions[body['action']](body, body['action'])
  except KeyError:
    raise NotImplementedError('Action %s not yet implemented' %(body['action']))
  except Exception as e:
    raise NotImplementedError(e)

class GithubRequestHandler(BaseHTTPRequestHandler):

  def do_POST(self):
    content_length = int(self.headers['Content-Length'])
    post_data = self.rfile.read(content_length)
    post_data_json = json.loads(post_data.decode('utf-8'))
    try:
      handle_action(post_data_json)
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.end_headers()
    except NotImplementedError as error:
      print(traceback.format_exc())
      self.send_error(501, str(error))
      self.send_header('Content-type', 'text/html')
      self.end_headers()
