import socket
from struct import *
import threading as thread
import time
import sys
import helper
from helper import Colors, QuestionBank

print(Colors.RED + f"hi there" + Colors.BLUE + f" wow" + Colors.RESET)
print("oh")

print( (Colors.BLUE + "Hello and welcome to the game!\n" 
                + f"Player 1: hi\n" 
                + f"Player 2: roi\n"  
                + "----------------------------------\n" 
                + Colors.GREEN + f"answer as fast as you can!! you have 10 seconds or until the other guys time:\n"
                + Colors.RED + f"(50 + 38 / 17)" + Colors.RESET))