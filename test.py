import socket
from struct import *
import threading as thread
import time
import sys
import helper
from helper import Colors, QuestionBank, GameStats

def packUdpPacket(port):
        return pack('=IbH', 0xabcddcba, 0x2, port)

pack = packUdpPacket(2069)
magic_cookie, msg_type, port_num = unpack('=IbH', pack)
if magic_cookie == 0xabcddcba and msg_type == 0x2:
    print("ok")