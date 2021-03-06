import socket
import threading as thread
from struct import *
import time
from helper import QuestionBank, Colors, GameStats

# t1 = thread.Thread(target = <function name>) - creating a thread
# t1.start() - starting the thread
# t1.join() - prevent from continuing until t1 has ended

# a class for the players of the game
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
        # for syncronizing
        self.condition = thread.Condition(thread.Lock())
        # for the bonus, supply statistics
        self.stats = GameStats()
    # packing the udp message
    def packUdpPacket(self, port):
        return pack('=IbH', 0xabcddcba, 0x2, port)
    # getting the name of the player, runs on a thread and with unblocked loop with sleep
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
    
    # waits for a message from the client for the game, runs unblocked for max 10 secs 
    def playerAnswer(self, player : Player, ans):
        socket = player.socket
        socket.setblocking(0)
        msg = None

        end = time.time() + 10.01
        while time.time() < end:
            if self.winner != None:
                socket.setblocking(1)
                return
            try: 
                msg = socket.recv(1024).decode("utf-8")
                msg = msg[0]
                if msg != None:
                    # we want lock this part of the code becuase we are determining the winner here
                    self.condition.acquire()
                    try:
                        # if there is a winner return
                        if self.winner != None:
                            self.condition.release()
                            socket.setblocking(1)
                            return
                        if (int(msg) <= 9) and (int(msg) >= 0): 
                            #we've got valid input
                            self.stats.addNumberOccurence(msg)
                        # checks if the answer is correct and sets the right winner
                        if int(msg) == ans:
                            self.winner = player.name
                        else:
                            if self.firstPlayer.name == player.name:
                                self.winner = self.secondPlayer.name
                            else:
                                self.winner = self.firstPlayer.name
                        self.stats.addPlayerPoint(self.winner)
                        self.condition.release()
                        return
                    except Exception as _:
                        self.condition.release()
            except Exception as _:
                pass
            time.sleep(0.1)
        socket.setblocking(1)
    # randomizing a question and making a message to send to the client 
    def startGame(self):
        q = self.bank.getQ()
        msg = (f"""
{self.stats.stats() + Colors.BLUE} 
Hello and welcome to the game!

Player 1: {self.firstPlayer.name} 
Player 2: {self.secondPlayer.name + Colors.RESET}  
---------------------------------- 
{Colors.GREEN}answer as fast as you can!! you have 10 seconds or until the other player's time:
{Colors.RED + q[0] + Colors.RESET}

""").encode("utf-8")
        print(msg.decode("utf-8")) 
        #generate math problam:
        self.firstPlayer.socket.send(msg)
        self.secondPlayer.socket.send(msg)
        # we want to wait for both threads of the answer to end before continuing 
        t1 = thread.Thread(target= self.playerAnswer, args = [self.firstPlayer, q[1]])
        t2 = thread.Thread(target= self.playerAnswer, args = [self.secondPlayer, q[1]])
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        if self.winner == None:
            msg = Colors.PURPLE + f"unfortunately, neither of you won, maybe try and answer faster next time!\nbtw, the correct answer was {q[1]}\n" + Colors.RESET
        else:
            msg = Colors.YELLOW + f"CONGRATULATION TO { self.winner }FOR THE WIN!\nthe correct answer was {q[1]}\n" + Colors.RESET
        msg = msg.encode("utf-8")
        self.firstPlayer.socket.send(msg)
        self.secondPlayer.socket.send(msg)
    
    # runs on a thread and sends offer requests for clients when there isnt two connected
    def offers(self, udpSocket : socket.socket):
        udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while self.firstPlayer == None or self.secondPlayer == None:
            udpSocket.sendto(self.packUdpPacket(self.port), (self.ip + ".255.255", 13117))
            time.sleep(1)
    
    # manages the main loop of the server, accepting clients and sending them to play
    def manage(self, welcomeSocket : socket.socket):
        #forever accepting clients
        t1, t2 = None, None

        # udp for sending broadcast
        udpSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
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
                if (self.firstPlayer.name not in (None, "", "\n")) and (self.secondPlayer.name not in (None, "", "\n")):
                    self.startGame()
                else:
                    # one didnt send their name so we are cancelling the game
                    res = "sorry, the game is cancelled, one player didnt enter their name. come again!".encode("utf-8")
                    try:
                        self.firstPlayer.socket.send(res)
                        self.secondPlayer.socket.send(res)
                    except Exception as _:
                        pass
                # done with the everything, reseting the fields
                try:
                    self.firstPlayer.socket.close()
                    self.secondPlayer.socket.close()
                except Exception as _:
                    pass
                # reseting data and offer thread for relunching the main loop
                self.firstPlayer, self.secondPlayer = None, None
                self.winner = None
                print(Colors.GREEN + "Game over, sending out offer requests..." + Colors.RESET)
                offerThread = thread.Thread(target = self.offers, args = [udpSocket])
                offerThread.start()
            except Exception as _:
                # if both player fields got set that means the offers stop, so we start them again
                if self.firstPlayer != None and self.secondPlayer != None:
                    offerThread = thread.Thread(target = self.offers, args = [udpSocket])
                    offerThread.start()
                if self.firstPlayer != None:
                    try:
                        self.firstPlayer.socket.send((Colors.RED + "sorry an error has occured, reconnect" + Colors.RESET).encode("utf-8"))
                        self.firstPlayer.socket.close()
                    except Exception as _:
                        pass
                    self.firstPlayer = None
                if self.secondPlayer != None:
                    try:
                        self.secondPlayer.socket.send((Colors.RED + "sorry an error has occured, reconnect" + Colors.RESET).encode("utf-8"))
                        self.secondPlayer.socket.close()
                    except Exception as _:
                        pass
                    self.secondPlayer = None

            
    # main run function of the server
    def run(self):

        # creating and binding the welcome socket
        welcomeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        welcomeSocket.bind((self.ip+".0.69", self.port))

        welcomeSocket.listen(1)

        # startup message  
        print(f"Server started, listening on IP address {self.ip}.0.69")

        # now need to manage accepts and at the same time send the udp offers.
        self.manage(welcomeSocket)




if __name__ == '__main__':
    ip = -1
    while ip == -1:
        ans = input("Hi! enter d for dev, t for test\n")
        if ans == "d":
            ip = "172.1"
        if ans == "t":
            ip = "172.99"
    server = Server(ip, 2069)
    server.run()
