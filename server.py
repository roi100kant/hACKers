import socket
import threading as thread
from struct import *
import time
from helper import QuestionBank, Colors

# t1 = thread.Thread(target = <function name>) - creating a thread
# t1.start() - starting the thread
# t1.join() - prevent from continuing until t1 has ended

class Player:
    def __init__(self, ip, port, socket : socket.socket):
        self.ip = ip
        self.port = port
        self.socket = socket
        self.name = None

    def setName(self, name):
        self.name = name

#server class
class Server:

    # init gets the ip and port for the server startup
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.firstPlayer = None
        self.secondPlayer = None
        self.winner = None
        self.bank = QuestionBank()
        self.condition = thread.Condition(thread.Lock())

    def packUdpPacket(self, port):
        return pack('IbH', 0xabcddcba, 0x2, port)

    def getName(self, player : Player):
        socket = player.socket
        socket.setblocking(0)
        msg = None

        end = time.time() + 10.01
        while time.time() < end:
            try: 
                msg = socket.recv(1024)
            except Exception as _:
                pass
            time.sleep(0.1)

        socket.setblocking(1)
        player.setName(msg.decode("utf-8"))

    def playerAnswer(self, player : Player, ans):
        socket = player.socket
        socket.setblocking(0)
        msg = None

        end = time.time() + 10.01
        while time.time() < end:
            try: 
                msg = socket.recv(1024).decode("utf-8")
                if msg != None:
                    self.condition.acquire()
                    if self.winner != None:
                        self.condition.release()
                        break
                    if int(msg) == ans:
                        self.winner = player.name
                    else:
                        if self.firstPlayer.name == player.name:
                            self.winner = self.secondPlayer.name
                        else:
                            self.winner = self.firstPlayer.name
                    self.condition.release()
                    break
            except Exception as _:
                pass
            time.sleep(0.1)

    def startGame(self):
        q = self.bank.getQ()
        print()
        msg = ("Hello and welcome to the game!\n" 
                + Colors.RED + f"Player 1: {self.firstPlayer.name}\n" 
                + f"Player 2: {self.secondPlayer.name}\n" + Colors.RESET  
                + Colors.BLUE + "----------------------------------\n" + Colors.RESET
                + f"answer as fast as you can, you have at most 10 seconds:\n"
                + Colors.GREEN + f"{q[0]}" + Colors.RESET).encode("utf-8")
        print(msg.decode("utf-8")) 
        #generate math problam:
        self.firstPlayer.socket.send(msg)
        self.secondPlayer.socket.send(msg)

        t1 = thread.Thread(target= self.playerAnswer, args = [self.firstPlayer, q[1]])
        t2 = thread.Thread(target= self.playerAnswer, args = [self.secondPlayer, q[1]])
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        msg = ""
        if self.winner == None:
            msg = f"unfortunately, neither of you won, maybe try and answer faster next time!\nthe correct answer was {q[1]}"
        else:
            msg = f"CONGRATULATION TO { self.winner } FOR THE WIN!\nthe correct answer was {q[1]}"

    def offers(self, udpSocket : socket.socket):
        udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while self.firstPlayer == None or self.secondPlayer == None:
            udpSocket.sendto(self.packUdpPacket(self.port), ("255.255.255.255", 13117))
            time.sleep(1)

    def manage(self, welcomeSocket : socket.socket):
        #forever accepting clients
        t1, t2 = None, None

        # udp for sending broadcast
        udpSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        offerThread = thread.Thread(target = self.offers, args = [udpSocket])
        offerThread.start()
        while True:
            try:
                numberOfConnections = 0
                while numberOfConnections < 2:
                    clientSock, clientAdd = welcomeSocket.accept()
                    print("player" , numberOfConnections+1, "connected")
                    if numberOfConnections == 0:
                        self.firstPlayer = Player(clientAdd[0], clientAdd[1], clientSock)
                        t1 = thread.Thread(target = self.getName, args = [self.firstPlayer])
                    else:
                        self.secondPlayer = Player(clientAdd[0], clientAdd[1], clientSock)
                        t2 = thread.Thread(target = self.getName, args = [self.secondPlayer])
                    numberOfConnections = numberOfConnections + 1
                t1.start()
                t2.start()
                t1.join()
                t2.join()
                if (self.firstPlayer.name != None) and (self.secondPlayer.name != None):
                    self.startGame()
                else:
                    # one didnt send their name so we are cancelling the game
                    res = "sorry, the game is cancelled, one player didnt enter their name. come again!".encode("utf-8")
                    try:
                        self.firstPlayer.socket.send(res)
                        self.secondPlayer.socket.send(res)
                    except:
                        pass
                # done with the everything, reseting the fields
                try:
                    self.firstPlayer.socket.close()
                    self.secondPlayer.socket.close()
                except Exception as _:
                    pass
                self.firstPlayer, self.secondPlayer = None, None
                self.winner = None
                print("Game over, sending out offer requests...")
                offerThread.start()
            except Exception as _:
                # if both player fields got set that means the offers stop, so we start them again
                if self.firstPlayer != None and self.secondPlayer != None:
                    offerThread.start()
                if self.firstPlayer != None:
                    try:
                        self.firstPlayer.socket.send("sorry an error has occured, reconnect")
                        self.firstPlayer.socket.close()
                    except Exception as _:
                        pass
                    self.firstPlayer = None
                if self.secondPlayer != None:
                    try:
                        self.secondPlayer.socket.send("sorry an error has occured, reconnect")
                        self.secondPlayer.socket.close()
                    except Exception as _:
                        pass
                    self.secondPlayer = None

            
    # main run function of the server
    def run(self):

        # creating and binding the welcome socket
        welcomeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        welcomeSocket.bind((self.ip, self.port))

        welcomeSocket.listen(1)

        # startup message  
        print(f"Server started, listening on IP address {self.ip}")

        # now need to manage accepts and at the same time send the udp offers.
        self.manage(welcomeSocket)




if __name__ == '__main__':
    ip = -1
    while ip == -1:
        ans = input("enter d for dev, t for test\n")
        if ans == "d":
            ip = "172.1.0.69"
        if ans == "t":
            ip = "172.99.0.69"
    server = Server(ip, 2070)
    server.run()