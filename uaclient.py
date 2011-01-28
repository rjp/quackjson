import httplib2
import json

class UAClient:
  base_uri = 'http://www.ua2.org/uaJSON'
  username = None
  password = None
  client = None

  def __init__(self, username = None, password = None, filename = None, debug = False):
    # If we're given a filename, parse that (as JSON) for the authentication details
    if filename:
      try:
        fp = open(filename, 'rb')
        try:
          contents = fp.read()
          data = json.loads(contents)
          self.username = data['username']
          self.password = data['password']
        finally:
          fp.close()
      except IOError:
        pass
    else:
      self.username = username
      self.password = password

    # You probably want to keep this on for development
    if (debug):
      httplib2.debuglevel = 1

    self.client = httplib2.Http()
    self.client.add_credentials(self.username, self.password)
  
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

  def get_folders(self, subscribed_only = False, unread_only = False):
    # Default is to fetch all folders
    path = '/folders'
    
    if subscribed_only:
      path += '/subscribed'
    else:
      path += '/all'
    
    if unread_only:
      path += '/unread'
    
    response, folders = self.send_request(path)
    
    return folders
  
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
