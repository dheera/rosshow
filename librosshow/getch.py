class Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

    def reset(self): return self.impl.reset()

class _GetchUnix:
    def __init__(self):
        import sys, tty, termios
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def reset(self):
        import sys, tty, termios
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

    def reset(self):
        return

getch = Getch()
