import curses
from uaclient import UAClient
from datetime import datetime

class qMenuOption:
  def __init__(self, character, description):
    self.character = character
    self.description = description

class qMenu:
  def __init__(self, name, options = None):
    self.options = []
    self.name = name
    
    if options:
      self.options = options

  def add_option(self, option):
    self.options.append(option)

class qUAck(UAClient):
  def __init__(self, username = None, password = None, filename = None, debug = False):
    UAClient.__init__(self, username = username, password = password, filename = filename, debug = debug)

    self.set_options()

    self.start_time = datetime.now()
    curses.wrapper(self.startcurses)
  
  def set_options(self):
    """ Set the options for this instance, reverting to defaults if not specified """
    if 'options' not in self.config:
      self.config['options'] = {}
    
    if 'menus' not in self.config['options']:
      self.config['options']['menus'] = 'expert'

  def print_menu_text(self, menu, elapsed_time = False):
    self.stdscr.addstr("\n")

    if elapsed_time:
      self.stdscr.addstr('+' + self.get_elapsed_time(), self.colours['yellow_black_bold'])
      self.stdscr.addstr(' ')

    self.stdscr.addstr(menu.name)
    
    if self.config['options']['menus'] == 'intermediate':
      self.stdscr.addstr(' (')
    
      for option in menu.options:
        self.stdscr.addstr(option.character.upper(), self.colours['yellow_black_bold'])
    
      self.stdscr.addstr(', ?+ for help)')
    
    self.stdscr.addstr(': ')
    self.stdscr.refresh()
    
  def print_menu_help(self, menu):
    self.stdscr.addstr("\nCommands:")
    
    for option in menu.options:
      self.stdscr.addstr("\n ")
      self.stdscr.addstr(option.character.upper(), self.colours['yellow_black_bold'])
      self.stdscr.addstr(' - ' + option.description)

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

  def startcurses(self, stdscr):
    curses.echo()
    self.setup_colours()
    self.stdscr = stdscr
    self.stdscr.scrollok(True)
    self.main_menu()
    curses.noecho()

  def setup_colours(self):
    self.colours = {}

    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    self.colours['yellow_black'] = curses.color_pair(1)
    self.colours['yellow_black_bold'] = self.colours['yellow_black'] | curses.A_BOLD

    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    self.colours['green_black'] = curses.color_pair(2)
    self.colours['green_black_bold'] = self.colours['green_black'] | curses.A_BOLD
    
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    self.colours['blue_black'] = curses.color_pair(3)
    self.colours['blue_black_bold'] = self.colours['blue_black'] | curses.A_BOLD
    
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    self.colours['cyan_black'] = curses.color_pair(4)
    self.colours['cyan_black_bold'] = self.colours['cyan_black'] | curses.A_BOLD

  def unrecognised_command(self):
    self.stdscr.addstr("\nUnrecognised command. Type ? for help")
    self.stdscr.refresh()
    
  def datetimeformat(self, timestamp, format):
    dt = datetime.fromtimestamp(int(timestamp))
    return dt.strftime(format)

  def main_menu(self):
    menu = qMenu('Main')
    menu.add_option(qMenuOption('j', 'Jump to folder / message'))
    menu.add_option(qMenuOption('l', 'List of folders'))
    menu.add_option(qMenuOption('q', 'Quit'))
    
    menu_continue = True

    while menu_continue:
      self.print_menu_text(menu, elapsed_time = True)

      c = self.stdscr.getch()

      if c == ord('q'):
        menu_continue = False
      elif c == ord('l'):
        self.folder_list_menu()
      elif c == ord('j'):
        self.jump_folder_message_menu()
      elif c == ord('?'):
        self.print_menu_help(menu)
      else:
        self.unrecognised_command()

  def folder_list_menu(self):
    menu = qMenu('Folders')
    menu.add_option(qMenuOption('a', 'All'))
    menu.add_option(qMenuOption('s', 'Subscribed'))
    menu.add_option(qMenuOption('x', 'eXit'))

    menu_continue = True

    while menu_continue:
      self.print_menu_text(menu)

      c = self.stdscr.getch()

      if c == ord('x'):
        menu_continue = False
      elif c == ord('a'):
        self.print_folder_list(self.get_folders())
        menu_continue = False
      elif c == ord('s'):
        self.print_folder_list(self.get_folders(subscribed_only = True))
        menu_continue = False
      elif c == ord('?'):
        self.print_menu_help(menu)
      else:
        self.unrecognised_command()

  def print_folder_list(self, folders):
    for folder in folders:
      self.stdscr.addstr("\n")
      self.stdscr.addstr(folder['folder'], self.colours['green_black_bold'])
      self.stdscr.refresh()

    self.stdscr.refresh()

  def jump_folder_message_menu(self):
    menu = qMenu('Jump')
    menu.add_option(qMenuOption('f', 'Folder'))
    menu.add_option(qMenuOption('m', 'Message'))
    menu.add_option(qMenuOption('x', 'eXit'))
    
    menu_continue = True
    
    while menu_continue:
      self.print_menu_text(menu)
      
      c = self.stdscr.getch()
     
      if c == ord('x'):
        menu_continue = False
        pass
      elif c == ord('f'):
        self.jump_folder_menu()
        menu_continue = False
      elif c == ord('m'):
        self.jump_message_menu()
        menu_continue = False
      elif c == ord('?'):
        self.print_menu_help(menu)
      else:
        self.unrecognised_command()
        menu_continue = False
        
  def jump_folder_menu(self):
    self.stdscr.addstr("\nFolder name (RETURN to abort): ")
    self.stdscr.refresh()
    folder_jump = self.stdscr.getstr()
    
    folder = self.get_folder(folder_jump)
    
    if folder is None:
      self.stdscr.addstr("\nNo such folder.")
      self.stdscr.refresh()
      
  def jump_message_menu(self):
    self.stdscr.addstr("\nMessage ID (RETURN to abort): ")
    self.stdscr.refresh()
    message_jump = self.stdscr.getstr()
    
    message = self.get_message(message_jump)
    
    if message is None:
      self.stdscr.addstr("\nNo such message.")
      self.stdscr.refresh()
    else:
      self.stdscr.addstr("\nMessage: ")
      self.stdscr.addstr(str(message['id']), self.colours['cyan_black_bold'])
      self.stdscr.addstr(" in ")
      self.stdscr.addstr(message['folder'], self.colours['cyan_black_bold'])
      
      self.stdscr.addstr("\nDate: ")
      self.stdscr.addstr(self.datetimeformat(message['epoch'], '%A, %d %B %Y - %H:%M:%S'), self.colours['green_black_bold'])
      
      self.stdscr.addstr("\nFrom: ")
      self.stdscr.addstr(message['from'], self.colours['green_black_bold'])
      
      if 'to' in message:
        self.stdscr.addstr("\nTo: ")
        self.stdscr.addstr(message['to'], self.colours['green_black_bold'])
      
      if 'subject' in message:
        if message['subject'] is not None: # better than a default subject?
          self.stdscr.addstr("\nSubject: ")
          self.stdscr.addstr(message['subject'], self.colours['green_black_bold'])
      
      if 'body' in message: # to be fair, this should always be true
        if message['body'] is None: # empty body is returned as NoneType, oddly
          message['body'] = ' '
        self.stdscr.addstr("\n\n" + message['body'] + "\n")
      
      self.stdscr.refresh()
