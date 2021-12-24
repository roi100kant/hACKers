import socket
import threading as thread

# t1 = thread.Thread(target = <function name>) - creating a thread
# t1.start() - starting the thread
# t1.join() - prevent from continuing until t1 has ended

#add a struct for the build of the udp message

#server class
class Server:

    # init gets the ip and port for the server startup
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port


    # will run of a thread and manage accepts from users
    # sends them to their own thread for the connection
    def manageAccepts(self, welcomeSocket):
        #forever accepting clients
        while True:
            clientSock, clientAdd = welcomeSocket.accept()


    # main run function of the server
    def run(self):

        # creating and binding the welcome socket
        welcomeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        welcomeSocket.bind((self.ip, self.port))

        # the size of the client listen queue
        welcomeSocket.listen(2)

        # startup message  
        print(f"Server started, listening on IP address {self.ip}")

        # now need to manage accepts and at the same time send the udp offers.




if __name__ == '__main__':
    server = Server(0,2069) # enter ip, port
    server.run()