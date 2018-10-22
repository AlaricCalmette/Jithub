import json
from http.server import HTTPServer
from jira import JIRA
from requestHandler import GithubRequestHandler

with open('serverConfig.json') as serverConfig:
  serverConfig_dict = json.load(serverConfig)
  SERVER_ADDRESS = (serverConfig_dict['address'], serverConfig_dict['port'])

httpd = HTTPServer(SERVER_ADDRESS, GithubRequestHandler)
httpd.serve_forever()
