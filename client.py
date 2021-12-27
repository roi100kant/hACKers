import socket
from struct import *

class Client:

    def __init__(self, ip):
        udpSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udpSocket.bind((ip, 13117)) #enter ip
        self.udpSocket = udpSocket
        self.ip = ip

    def unpackUdpPacket(self, packet):
        return unpack('IbH', packet)

    # main function of the client
    def run(self):
        while 1:
            try:
                # recieve the info and unpack it
                packet = self.udpSocket.recv(1024)
                magic_cookie, msg_type, port_num = self.unpackUdpPacket(packet)
                
                # check corectness and if so try and connect and play the game
                if magic_cookie == 0xabcddcba and msg_type == 0x2:
                    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        print(f"Received offer from {self.ip}, attempting to connect...")
                        tcpSocket.connect((self.ip, port_num))
                        self.handleGame(tcpSocket)
                    except Exception as _:
                        pass
                    finally:
                        tcpSocket.close()
            except Exception as _:
                pass

    def nonBlockingCheckResponse(self, tcpSocket : socket.socket):
        import sys, select, tty, termios, time

        global userRes, serverRes
        userRes, serverRes = None, None

        #returns if the stdin is ready to be read from (there is a character there)
        def isData():
            return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

        # try to get msg from the server
        def gameResponse():
            global serverRes
            try:
                tcpSocket.setblocking(0)
                response = tcpSocket.recv(1024)
                serverRes = response.decode("utf-8")
            except Exception as _:
                pass
            finally:
                tcpSocket.setblocking(1)
        
        # the old settings of the stdin
        old_settings = termios.tcgetattr(sys.stdin)

        try:
            # places terminal into a character break
            tty.setcbreak(sys.stdin.fileno())
            
            #our main loop, works for ten seconds, trying to get response from server and user and then sleep
            t_end = time.time() + 10.01
            while time.time() < t_end:
                gameResponse()
                if isData():
                    userRes = sys.stdin.read(1)
                    print("You pressed", userRes)

                if serverRes != None:
                    print(serverRes)
                    break
                
                if userRes != None:
                    tcpSocket.send(userRes.encode("utf-8"))
                    res = tcpSocket.recv(1024)
                    print(res.decode("utf-8"))
                    break
                time.sleep(0.1)

        finally:
            #return the old settings 
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    #in this state we are connected to the server and are about to play the game
    def handleGame(self, tcpSocket : socket.socket):
        # first step, send our name to the server 
        tcpSocket.send("hACKers")

        # then we need to wait for the server rsponse over tcp
        # and then print the message to the human players
        question = tcpSocket.recv(1024)
        print(question.decode("utf-8"))

        #handles the part where we wait for the user to enter or server to respond
        self.nonBlockingCheckResponse(tcpSocket)

   
if __name__ == '__main__':
    ip = -1
    while ip == -1:
        ans = input("enter d for dev, t for test")
        if ans == "d":
            ip = "172.1.0.69"
        if ans == "t":
            ip = "172.99.0.69"
    client = Client(ip)
    client.run()




