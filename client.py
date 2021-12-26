import socket
from struct import *

class Client:

    def __init__(self):
        udpSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udpSocket.bind((socket.gethostbyname(socket.gethostname()), 13117)) #enter ip
        self.udpSocket = udpSocket

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

    #in this state we are connected to the server and are about to play the game
    def handleGame(self, tcpSocket : socket.socket):
        
        # first step, send our name to the server 
        tcpSocket.send("hACKers")

        # then we need to wait for the server rsponse over tcp
        # and then print the message to the human players
        question = tcpSocket.recv(1024)
        print(question.decode("utf-8"))

        # next steps are:
        # allow the user to enter their answer to the question
        # send the answer to the server
        # wait for the server response regarding the answer
        # go back to searching offers

        # IMPORTANT: we need to handle the case where we get the answer
        # but the other player answered before us so the server sent us a message 
        # before we send our own answer (we are single thread)
        self.run()

   
if __name__ == '__main__':
    client = Client()
    client.run()




