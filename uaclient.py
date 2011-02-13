import httplib2
import json

class UAClient:
  # Base URI - must not include trailing slash
  base_uri = 'http://www.ua2.org/uaJSON'
  client = None
  
  config = {}
  cache = {}

  def __init__(self, username = None, password = None, filename = None, debug = False):
    # If we're given a filename, parse that (as JSON) for the authentication details
    if filename:
      try:
        fp = open(filename, 'rb')
        try:
          contents = fp.read()
          self.config = json.loads(contents)
        finally:
          fp.close()
      except IOError:
        pass
    else:
      self.config['username'] = username
      self.config['password'] = password

    if 'base_uri' in self.config:
        self.base_uri = self.config['base_uri']

    # You probably want to keep this on for development
    if (debug):
      httplib2.debuglevel = 1

    self.client = httplib2.Http()
    self.client.add_credentials(self.config['username'], self.config['password'])
    
    # Initialise cache
    self.update_cache()

  def send_request(self, path, method = 'GET', params = {}, body = None):
    uri = self.base_uri + path

    headers = {}
    headers['Accept'] = 'application/json'

    if method == 'GET':
      response, data = self.client.request(uri, 'GET', headers = headers)
    elif method == 'POST':
      headers['Content-Type'] = 'application/json'    
      response, data = self.client.request(uri, 'POST', body = body, headers = headers)

    data = json.loads(data)

    return response, data

  def update_cache(self):
    if 'folders' not in self.cache:
      path = '/folders'

      response, self.cache['folders'] = self.send_request(path)

  def get_folders(self, subscribed_only = False, unread_only = False):
    folders = self.cache['folders']
    
    # No need to check for subscribed only *and* unread only, as we are always reducing the size
    # of 'folders'
    if subscribed_only:
      folders = [folder for folder in folders if folder['subscribed'] is True]

    if unread_only:
      folders = [folder for folder in folders if folder['unread'] >= 1]

    return folders

  def get_folder(self, name):
    name = name.lower()
    folders = [folder for folder in self.cache['folders'] if folder['folder'].lower() == name]
    
    if len(folders) == 1:
      return folders[0]
    else:
      return None

  def get_folder_message_list(self, folder, unread_only = True):
    path = '/folder/' + folder

    if unread_only:
      path += '/unread'

    response, messages = self.send_request(path)

    return messages

  def get_folder_messages(self, folder, unread_only = True):
    message_list = self.get_folder_message_list(folder, unread_only)

    messages = []

    for message in message_list:
      messages.append(self.get_message(message['id']))

    return messages

  def get_message(self, id):
    path = '/message/' + str(id)

    response, message = self.send_request(path)
    
    if response.status == 404:
      # Possibly better throwing an exception here
      return None

    return message

  def post_message(self, folder, subject, body, to = '',):
    message = {}
    message['subject'] = subject
    message['to'] = to
    message['body'] = body

    body = json.dumps(message)

    path = '/folder/' + folder

    response, data = self.send_request(path, method = 'POST', body = body)

  def change_subscription(self, folder, change):
    subscription = {}
    subscription['folder'] = folder

    body = json.dumps(subscription)

    path = '/folder/' + folder + '/' + change

    response, data = self.send_request(path, method = 'POST', body = body)

    return response, data

  def subscribe(self, folder):
    return self.change_subscription(folder, 'subscribe')

  def unsubscribe(self, folder):
    return self.change_subscription(folder, 'unsubscribe')
