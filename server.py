import json
import os
from http.server import HTTPServer
from requestHandler import GithubRequestHandler

with open('serverConfig.json') as serverConfig:
  serverConfig_dict = json.load(serverConfig)
  SERVER_ADDRESS = (serverConfig_dict['address'], int(os.environ['PORT']))

httpd = HTTPServer(SERVER_ADDRESS, GithubRequestHandler)
httpd.serve_forever()
