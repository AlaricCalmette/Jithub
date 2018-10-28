import json
from oauthlib.oauth1 import SIGNATURE_RSA
from requests_oauthlib import OAuth1Session

def read(file_path):
  """ Read a file and return it's contents. """
  with open(file_path) as f:
    return f.read()

# The Consumer Key created while setting up the "Incoming Authentication" in
# JIRA for the Application Link.

with open('config.json') as config_file:
  config = json.load(config_file)

CONSUMER_KEY = config['jira']['consumer_key']

# The contents of the rsa.pem file generated (the private RSA key)
RSA_KEY = read(config['jira']['cert_path'])

# The URLs for the JIRA instance
JIRA_SERVER = config['jira']['instance_address']
REQUEST_TOKEN_URL = JIRA_SERVER + '/plugins/servlet/oauth/request-token'
AUTHORIZE_URL = JIRA_SERVER + '/plugins/servlet/oauth/authorize'
ACCESS_TOKEN_URL = JIRA_SERVER + '/plugins/servlet/oauth/access-token'


# Step 1: Get a request token

oauth = OAuth1Session(CONSUMER_KEY, signature_type='auth_header',
                      signature_method=SIGNATURE_RSA, rsa_key=RSA_KEY, verifier='blah')
request_token = oauth.fetch_request_token(REQUEST_TOKEN_URL)

# Step 2: Get the end-user's authorization
print("  Visit to the following URL to provide authorization:")
print("  {}?oauth_token={}".format(AUTHORIZE_URL, request_token['oauth_token']))
print("\n")

while input("Press any key to continue..."):
  pass


# Step 3: Get the access token

access_token = oauth.fetch_access_token(ACCESS_TOKEN_URL)
config['jira']['oauth_token'] = access_token['oauth_token']
config['jira']['oauth_secret'] = access_token['oauth_token_secret']
with open('config.json', 'w') as config_file:
  json.dump(config, config_file, indent=4)
