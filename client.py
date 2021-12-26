import socket
from struct import *
import threading as thread

from assist import Assist

#the main thread
mainT = thread.main_thread()

class Client:

    def __init__(self):
        udpSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udpSocket.bind((socket.gethostbyname(socket.gethostname()), 13117)) #enter ip
        self.udpSocket = udpSocket
        self.assist = Assist(thread.Condition(thread.Lock()))

    # reads one char from the user without pressing enter
    def readAnswer(self):
        global userAns
        # three imports that are needed only for read
        import tty, sys, termios
        filedescriptors = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin)
        userAns=sys.stdin.read(1)[0]
        print("You pressed", userAns)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN,filedescriptors)
        self.assist.wakeUp()

    def unpackUdpPacket(self, packet):
        return unpack('IbH', packet)

    # main function of the client
    def run(self):
        while 1:
            try:
                # recieve the info and unpack it
                packet, IPnPort = self.udpSocket.recvfrom(1024)
                magic_cookie, msg_type, port_num = self.unpackUdpPacket(packet)
                
                # check corectness and if so try and connect and play the game
                if magic_cookie == 0xabcddcba and msg_type == 0x2:
                    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        tcpSocket.connect((IPnPort[0], port_num))
                        self.handleGame(tcpSocket)
                    except Exception as _:
                        pass
                    finally:
                        tcpSocket.close()
            except Exception as _:
                pass

    def gameResponse(self, tcpSocket : socket.socket):
        global serverRes
        try:
            response = tcpSocket.recv(1024)
            serverRes = response.decode("utf-8")
            self.assist.wakeUp()
        except Exception as _:
            pass


    #in this state we are connected to the server and are about to play the game
    def handleGame(self, tcpSocket : socket.socket):
        global userAns, serverRes
        userAns, serverRes = None, None
        # first step, send our name to the server 
        tcpSocket.send("hACKers")

        # then we need to wait for the server rsponse over tcp
        # and then print the message to the human players
        question = tcpSocket.recv(1024)
        print(question.decode("utf-8"))

        inputThread = thread.Thread(target = self.readAnswer)
        serverThread = thread.Thread(target = self.gameResponse)

        inputThread.start()
        serverThread.start()
        self.assist.wait(10)




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
    client.run()




