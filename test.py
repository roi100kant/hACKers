import socket
from struct import *
import threading as thread
import time
import sys
import helper
from helper import Colors, QuestionBank, GameStats


print(Colors.RED + "text\n")

stats = GameStats()
stats.addPlayerPoint("p1")
stats.addPlayerPoint("p2")
stats.addPlayerPoint("p1")
stats.addPlayerPoint("p3")
stats.addPlayerPoint("p2")
stats.addPlayerPoint("p3")
stats.addPlayerPoint("p1")
stats.addPlayerPoint("p1")
stats.addPlayerPoint("p3")
stats.addNumberOccurence("1")
stats.addNumberOccurence("2")
stats.addNumberOccurence("3")
stats.addNumberOccurence("2")
stats.addNumberOccurence("1")
stats.addNumberOccurence("1")

print(stats.stats() + Colors.BLUE + "Hello and welcome to the game!\n" 
                + f"Player 1: roi\n" 
                + f"Player 2: david\n"  
                + "----------------------------------\n" 
                + Colors.GREEN + f"answer as fast as you can!! you have 10 seconds or until the other guys time:\n"
                + Colors.RED + f"1 + 1" + Colors.RESET)