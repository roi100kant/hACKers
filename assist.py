class Assist:

    def __init__(self, cond):
        self.condition = cond

    def wakeUp(self):
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()

    def wait(self, time):
        self.condition.acquire()
        self.condition.wait(time)
        self.condition.release()