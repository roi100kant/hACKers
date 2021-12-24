import socket

#add a struct for the build of the udp message

class Client:

    def __init__(self):
        self.udpSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def searchServer(self):

        msg = self.udpSocket.recvfrom()
        # check packet format
        # extract port of the server
        # try to connect to the server
        # if succeeds move to different func to send username and prepare for game
        # if fails go to run again to await another offer

    #in this state we are connected to the server and are about to play the game
    def handleGame(self, tcpSocket : socket.socket):
        
        # first step, send our name to the server 
        tcpSocket.send("<enter our name here>")

        # then we need to wait for the server rsponse with the question
        # and then print the message to the users of the client
        msg = tcpSocket.recv(1024)
        print(msg.decode("utf-8"))

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
    client.searchServer()




