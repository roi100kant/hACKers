class Assist:

    def __init__(self, cond):
        self.condition = cond

    # waking up the thread asleep because of wait
    def wakeUp(self):
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()

    # applying wait to the current thread
    def wait(self, time):
        self.condition.acquire()
        self.condition.wait(time)
        self.condition.release()

    #read a character from screen - blocking
    def readAnswer(self):
        # three imports that are needed only for read
        import tty, sys, termios
        filedescriptors = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin)
        userAns=sys.stdin.read(1)[0]
        print("You pressed", userAns)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN,filedescriptors)