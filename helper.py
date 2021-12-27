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
        self.questions = [("17 * 2 - 29", 5), ("(45 + 54) / 11", 9), ("(35 + 27 - 18) / 11", 4), ("2 + 3", 5),
                          ("(40 + 40) / 10"), ("1+2+5-6", 2), ("3!", 6), ("(34 - 12 + 17 - 9) * 0", 0),
                          ("(72 - 2 - 10 - 20) / 10 ", 4), ("42 / 7", 6), ("0.5 * 0.5 * 4", 1), ("1 + 1 + 1 + 1 + 1 + 1 * 0 + 1 + 1", 7),
                          ("e^0", 1), ("ln(1)", 0), ("ln(e)", 1), ("ln(1/e) + 1", 0), ("f(x)=x^2, f'(2)=?", 7),
                          ("f'(x)=2x, f(3)=?", 9), ("2x+3 = 7", 2), ("7x - 6 = 8", 2)]
    def getQ(self):
        return self.questions[random.randint(0, len(self.questions)-1)]
