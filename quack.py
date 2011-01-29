from uaclient import UAClient
from datetime import datetime

class qUAck(UAClient):
  unrecognised_command = 'Unrecognised command. Type ? for help'

  def __init__(self, username = None, password = None, filename = None, debug = False):
    UAClient.__init__(self, username = username, password = password, filename = filename, debug = debug)

    self.start_time = datetime.now()

  def get_menu_text(self):
    return '+' + self.get_elapsed_time() + ' Main (BCDE, ?+ for help): '

  def get_elapsed_time(self):
    current_time = datetime.now()
    time_diff = current_time - self.start_time

    minutes, seconds = divmod(time_diff.seconds, 60)
    hours, minutes = divmod(minutes, 60)

    # Convert to string and pad with zeroes
    hours = str(hours).zfill(2)
    minutes = str(minutes).zfill(2)

    elapsed_time = hours + ':' + minutes

    return elapsed_time
