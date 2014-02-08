import SocketServer
import threading

class TestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        while True:
            self.data = self.request.recv(1024).strip()
            print "{}:".format(self.client_address[0])
            print self.data
            self.request.sendall(self.data.upper() + '\n')

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == '__main__':
    HOST, PORT = "localhost", 7777
    server = ThreadedTCPServer((HOST, PORT), TestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.deamon = True
    server_thread.start()
    input("Press enter to shutdown")
    server.shutdown()
    