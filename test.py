import socket
from struct import *
import threading as thread
import time

def nonBlockingKeyRead():
        global userAns
        import sys, select, tty, termios, time
        #returns if the stdin is ready to be read from (there is a character there)
        def isData():
            return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            # places terminal into a character break
            tty.setcbreak(sys.stdin.fileno())
            #loop waiting for user input
            while 1:
                time.sleep(0.1)
                print("hi")
                if isData():
                    userAns = sys.stdin.read(1)
                    print("You pressed", userAns)
                    break
        finally:
            #return the old settings 
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


nonBlockingKeyRead()
print("hello")




