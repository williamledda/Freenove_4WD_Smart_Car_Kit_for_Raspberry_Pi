import os
import sys
from Thread import *
from threading import Thread
from server import Server
from PyQt5.QtCore import QCoreApplication


class CarServer:
    def __init__(self):
        self.TCP_Server = Server()

    def start(self):
        print("Open TCP")
        self.TCP_Server.StartTcpServer()
        self.ReadData = Thread(target=self.TCP_Server.readdata)
        self.SendVideo = Thread(target=self.TCP_Server.sendvideo)
        self.power = Thread(target=self.TCP_Server.Power)
        self.SendVideo.start()
        self.ReadData.start()
        self.power.start()

    def close(self):
        try:
           stop_thread(self.SendVideo)
           stop_thread(self.ReadData)
           stop_thread(self.power)
        except:
            pass
        try:
            self.TCP_Server.server_socket.shutdown(2)
            self.TCP_Server.server_socket1.shutdown(2)
            self.TCP_Server.StopTcpServer()
        except:
            pass
        print ("Close TCP")
        QCoreApplication.instance().quit()
        os._exit(0)


if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    server = CarServer()
    try:
        server.start()
        while True:
            pass
    except KeyboardInterrupt:
        server.close()
