import curses
from quack import qUAck

def duck(stdscr):
  client = qUAck(filename = 'quackrc')	
  stdscr.addstr(client.get_menu_text())
  stdscr.refresh()

  menu_continue = True

  while menu_continue:
    c = stdscr.getch()

    if c == ord('l') or c == ord('L'):
      stdscr.addstr("\nList of folders")
      stdscr.addstr("\n"+client.get_menu_text())
    elif c == ord('q') or c == ord('Q'):
      menu_continue = False
    else:
      stdscr.addstr("\n"+client.unrecognised_command)
      stdscr.addstr("\n"+client.get_menu_text())

    stdscr.refresh()

curses.wrapper(duck)
