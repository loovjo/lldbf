from colorama import Fore, Back, Style, init
init()

COL_RESET = Style.RESET_ALL

COL_INFO = Fore.BLUE
COL_MARKER = Fore.GREEN
COL_ERROR = Fore.RED
COL_WARN = Fore.MAGENTA

def var(name):
    return "`" + name + "`"

def type_(name):
    return "`" + name + "`"

macro = var

def marker(ch):
    return COL_MARKER + ch + COL_RESET

def note(note):
    return COL_INFO + note + COL_RESET

def error(error):
    return COL_ERROR + error + COL_RESET

def warning(error):
    return COL_WARN + error + COL_RESET

def file_location(filename, start_line, end_line):
    text = "in " + filename
    if start_line == end_line:
        text += ":" + str(start_line)
    else:
        text += ":" + str(start_line) + ".." + str(end_line)
    return COL_INFO + text + COL_RESET
