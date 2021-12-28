import socket
from struct import *
import threading as thread
import time
import sys
import helper
from helper import Colors, QuestionBank

print(Colors.RED + f"hi there" + Colors.BLUE + f" wow" + Colors.RESET)

dict = {"1" : 3, "2" : 2}
print(dict)
dict["3"] = 3
dict["1"] = 3

t = ["r", "0"]
t[0] = "f"
