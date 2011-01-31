import curses
from uaclient import UAClient
from datetime import datetime

class qUAck(UAClient):
  def __init__(self, username = None, password = None, filename = None, debug = False):
    UAClient.__init__(self, username = username, password = password, filename = filename, debug = debug)

    self.start_time = datetime.now()
    curses.wrapper(self.startcurses)

  def print_menu_text(self, menu, char_options, elapsed_time = False):
    self.stdscr.addstr("\n")

    if elapsed_time:
      self.stdscr.addstr('+' + self.get_elapsed_time(), self.colours['yellow_black_bold'])
      self.stdscr.addstr(' ')

    self.stdscr.addstr(menu)
    self.stdscr.addstr(' (')
    self.stdscr.addstr(''.join(char_options).upper(), self.colours['yellow_black_bold'])
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
    self.setup_colours()
    self.stdscr = stdscr
    self.stdscr.scrollok(True)
    self.main_menu()

  def setup_colours(self):
    self.colours = {}

    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    self.colours['yellow_black'] = curses.color_pair(1)
    self.colours['yellow_black_bold'] = self.colours['yellow_black'] | curses.A_BOLD

    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    self.colours['green_black'] = curses.color_pair(2)
    self.colours['green_black_bold'] = self.colours['green_black'] | curses.A_BOLD

  def unrecognised_command(self):
    self.stdscr.addstr("\nUnrecognised command. Type ? for help")
    self.stdscr.refresh()

  def main_menu(self):
    char_options = ['l', 'q']
    menu_continue = True

    while menu_continue:
      self.print_menu_text('Main', char_options, elapsed_time = True)

      c = self.stdscr.getch()

      if c == ord('q'):
        menu_continue = False
      elif c == ord('l'):
        self.folder_list_menu()
      else:
        self.unrecognised_command()

  def folder_list_menu(self):
    char_options = ['a', 's', 'x']
    menu_continue = True

    while menu_continue:
      self.print_menu_text('Folders', char_options)

      c = self.stdscr.getch()

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
      self.stdscr.addstr("\n")
      self.stdscr.addstr(folder['folder'], self.colours['green_black_bold'])
      self.stdscr.refresh()

    self.stdscr.refresh()
