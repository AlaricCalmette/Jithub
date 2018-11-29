import json
import re
from jira import JIRA

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
