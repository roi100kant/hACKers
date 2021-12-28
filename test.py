import socket
from struct import *
import threading as thread
import time
import sys
import helper
from helper import Colors, QuestionBank

print(Colors.RED + f"hi there" + Colors.BLUE + f" wow" + Colors.RESET)
print("oh")

print(pack('IbH', 0xabcddcba, 0x2, 2069))