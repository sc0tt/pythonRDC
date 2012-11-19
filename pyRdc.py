import sys
import ConfigParser
import pyRDCItem
from PySide import QtCore, QtGui
from PySide.QtUiTools import QUiLoader

class pyRDC(QtGui.QWidget):
    def __init__(self):
        super(pyRDC, self).__init__()
        self.servers = []
        layout_loader = QUiLoader()
        layout_file = QtCore.QFile("resources/rdc.ui")
        layout_file.open(QtCore.QFile.ReadOnly)
        self.ui = layout_loader.load(layout_file)
        self.ui.show()

        self.ui.pbAdd.clicked.connect(self.add_server)
        self.ui.pbConnect.clicked.connect(self.connect)
        self.ui.actionSave.triggered.connect(self.save_conf)

        self.config = ConfigParser.RawConfigParser()
        self.load_config()

    def load_config(self):
        if self.config.read("servers.cfg"):
            for section in self.config.sections():
                print section

    def add_server(self):
        title = self.ui.leDisplayName.text()
        ip = self.ui.leIP.text()
        port = self.ui.lePort.text()
        width = self.ui.leWidth.text()
        height = self.ui.leHeight.text()
        fs = True if self.ui.cbFullScreen.checkState() == QtCore.Qt.CheckState.Checked else False
        self.servers.append(pyRDCItem.pyRDCItem(title, ip, port, width, height, fs))
        print self.servers


    def connect(self):
        pass

    def rem_server(self):
        pass

    def save_conf(self):
        for server in self.servers:
            if not self.config.has_section(server.title):
                self.config.add_section(server.title)
            self.config.set(server.title, "ip", server.ip)
            self.config.set(server.title, "port", server.port)
            self.config.set(server.title, "width", server.width)
            self.config.set(server.title, "height", server.height)
            self.config.set(server.title, "fs", server.fs)

        with open('servers.cfg', 'wb+') as tmp_config:
            self.config.write(tmp_config)

    def exit(self):
        pass




def main():
    app = QtGui.QApplication(sys.argv)
    ex = pyRDC()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()