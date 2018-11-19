from http.server import BaseHTTPRequestHandler
import json
from handle_labeled_unlabeled import handle_labeled_unlabeled

with open('config.json') as config:
  config_dict = json.load(config)

def handle_action(body):
  actions = {
    'labeled': handle_labeled_unlabeled,
    'unlabeled': handle_labeled_unlabeled
  }
  try:
    actions[body['action']](body)
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
      self.send_error(501, str(error))
      self.send_header('Content-type', 'text/html')
      self.end_headers()
