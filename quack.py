import curses
from uaclient import UAClient
from datetime import datetime

class qUAck(UAClient):
  yellow_black = 1

  def __init__(self, username = None, password = None, filename = None, debug = False):
    UAClient.__init__(self, username = username, password = password, filename = filename, debug = debug)

    self.start_time = datetime.now()
    curses.wrapper(self.startcurses)

  def print_menu_text(self, menu, char_options, elapsed_time = False):
    self.stdscr.addstr("\n")

    if elapsed_time:
      self.stdscr.addstr('+' + self.get_elapsed_time(), curses.color_pair(self.yellow_black))
      self.stdscr.addstr(' ')

    self.stdscr.addstr(menu)
    self.stdscr.addstr(' (')
    self.stdscr.addstr(''.join(char_options).upper(), curses.color_pair(self.yellow_black))
    self.stdscr.addstr(', ?+ for help): ')
    self.stdscr.refresh()

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
    curses.init_pair(self.yellow_black, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    self.stdscr = stdscr
    self.main_menu()

  def unrecognised_command(self):
    self.stdscr.addstr("\nUnrecognised command. Type ? for help")
    self.stdscr.refresh()

  # Convert character options to menu options
  def get_menu_options(self, options):
    menu_options = []

    for option in options:
      menu_options.append(ord(option))

    return menu_options

  def main_menu(self):
    char_options = ['l', 'q']
    menu_options = self.get_menu_options(char_options)
    menu_continue = True

    while menu_continue:
      self.print_menu_text('Main', char_options, elapsed_time = True)

      c = self.stdscr.getch()

      if c in menu_options:
        if c == ord('q'):
          menu_continue = False
        elif c == ord('l'):
          self.folder_list_menu()
      else:
        self.unrecognised_command()

  def folder_list_menu(self):
    char_options = ['a', 's', 'x']
    menu_options = self.get_menu_options(char_options)
    menu_continue = True

    while menu_continue:
      self.print_menu_text('Folders', char_options)

      c = self.stdscr.getch()

      if c in menu_options:
        if c == ord('x'):
          menu_continue = False
        elif c == ord('a'):
          self.print_folder_list(self.get_folders())
          menu_continue = False
        elif c == ord('s'):
          self.print_folder_list(self.get_folders(subscribed_only = True))
          menu_continue = False
      else:
        self.unrecognised_command()

  def print_folder_list(self, folders):
    for folder in folders:
      self.stdscr.addstr("\n" + folder['folder'])
      self.stdscr.refresh()

    self.stdscr.refresh()
