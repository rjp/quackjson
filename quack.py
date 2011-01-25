from uaclient import UAClient

class qUAck(UAClient):
  def __init__(self, username = None, password = None, filename = None):
    UAClient.__init__(self, username = username, password = password, filename = filename)
    