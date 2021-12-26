import socket
from struct import *
import threading as thread
import time

from assist import Assist

#the main thread
mainT = thread.main_thread()

class Client:

    def __init__(self):
        self.assist = Assist(thread.Condition(thread.Lock()))

    # reads one char from the user without pressing enter
    def readAnswer(self):
        try:
            time.sleep(1)
            self.assist.wakeUp()
        except Exception as _:
            pass

    def gameResponse(self):
        try:
            time.sleep(1)
            self.assist.wakeUp()
        except Exception as _:
            pass


    #in this state we are connected to the server and are about to play the game
    def handleGame(self):
        inputThread = thread.Thread(target = self.readAnswer)
        serverThread = thread.Thread(target = self.gameResponse)

        inputThread.start()
        serverThread.start()
        print("down")
        self.assist.wait(100)
        print("up")



        # next steps are:
        # allow the user to enter their answer to the question
        # send the answer to the server
        # wait for the server response regarding the answer
        # go back to searching offers

        # IMPORTANT: we need to handle the case where we get the answer
        # but the other player answered before us so the server sent us a message 
        # before we send our own answer (we are single thread)

   
if __name__ == '__main__':
    client = Client()
    client.handleGame()
    print("done")




