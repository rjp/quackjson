from formatter import NullWriter
import re

class StringWriter(NullWriter):
    def __init__(self, maxcol=72):
        self.lines = []
        self.maxcol = maxcol
        NullWriter.__init__(self)
        self.reset()

    def reset(self):
        self.col = 0
        self.atbreak = 0

    def send_paragraph(self, blankline):
        self.lines.append('\n'*blankline)
        self.col = 0
        self.atbreak = 0

    def send_line_break(self):
        self.lines.append('\n')
        self.col = 0
        self.atbreak = 0

    def send_hor_rule(self, *args, **kw):
        self.lines.append('\n')
        self.lines.append('-'*self.maxcol)
        self.lines.append('\n')
        self.col = 0
        self.atbreak = 0

    def send_literal_data(self, data):
        self.lines.append(data)
        i = data.rfind('\n')
        if i >= 0:
            self.col = 0
            data = data[i+1:]
        data = data.expandtabs()
        self.col = self.col + len(data)
        self.atbreak = 0

    def send_flowing_data(self, data):
        if not data: return
        atbreak = self.atbreak or data[0].isspace()
        col = self.col
        maxcol = self.maxcol
        write = self.lines.append
        for word in data.split():
            if atbreak:
                if col + len(word) >= maxcol:
                    write('\n')
                    col = 0
                else:
                    write(' ')
                    col = col + 1
            write(word)
            col = col + len(word)
            atbreak = 1
        self.col = col
        self.atbreak = data[-1].isspace()

    def output(self):
        return "".join(self.lines)

def linebreak(text, width):
    a = StringWriter(width)
    lines = text.replace("\r","").split("\n")
    state = None

    for line in lines:
        if (re.match(r'^>', line) or re.match(r'^ ', line)):
            if state == 'sfd':
                a.send_paragraph(2)
            a.send_literal_data(line)
            a.send_line_break()
            state = 'sld'
        else:
            if len(line) == 0:
                if state == 'sld':
                    a.send_paragraph(1)
                else:
                    a.send_paragraph(2)
                state = 'sp'
            else:
                if state == 'sfd':
                    a.send_flowing_data(' ')
                a.send_flowing_data(line)
                state = 'sfd'

    return a.output()
