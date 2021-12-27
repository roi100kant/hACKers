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

import random
class QuestionBank:
    
    def __init__(self):
        self.questions = [["17*2 - 29", 5], ["(45 + 54) / 11", 9]

                        ]
    def getQ(self):
        return self.questions[random.randint(0, len(self.questions)-1)]
