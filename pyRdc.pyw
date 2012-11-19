import sys
import ConfigParser
import pyRDCItem
import subprocess
from PySide import QtCore, QtGui
from PySide.QtUiTools import QUiLoader
import pyRDC_resources


class pyRDC(QtGui.QWidget):
    def __init__(self):
        super(pyRDC, self).__init__()
        self.servers = {}
        layout_loader = QUiLoader()
        layout_file = QtCore.QFile(":resources/rdc.ui")
        layout_file.open(QtCore.QFile.ReadOnly)
        self.ui = layout_loader.load(layout_file)
        self.index = None

        self.icon = QtGui.QIcon(":resources/icon.png")

        self.ui.show()

        self.ui.pbAdd.clicked.connect(self.add_server)
        self.ui.pbRemove.clicked.connect(self.rem_server)
        self.ui.pbConnect.clicked.connect(self.connect)
        self.ui.actionSave.triggered.connect(self.save_conf)
        self.ui.cbServers.activated.connect(self.load_server)

        self.config = ConfigParser.RawConfigParser()
        self.load_config()

    def load_config(self):
        if self.config.read("servers.cfg"):
            for section in self.config.sections():
                ip = self.config.get(section, "ip")
                port = self.config.get(section, "port")
                width = self.config.get(section, "width")
                height = self.config.get(section, "height")
                fs = self.config.get(section, "fs")
                item = pyRDCItem.pyRDCItem(section, ip, port, width, height, fs)
                self.servers[section] = item
                self.ui.cbServers.addItem(self.icon, section)

    def add_server(self):
        title = self.ui.leDisplayName.text()
        ip = self.ui.leIP.text()
        port = self.ui.lePort.text()
        width = self.ui.leWidth.text()
        height = self.ui.leHeight.text()
        fs = True if self.ui.cbFullScreen.checkState() == QtCore.Qt.CheckState.Checked else False
        item = pyRDCItem.pyRDCItem(title, ip, port, width, height, fs)
        self.servers[title] = item
        if self.ui.cbServers.findText(title) == -1:
            self.ui.cbServers.addItem(self.icon, title)

        self.clear_form()

    def connect(self):
        server = self.get_selected_server()
        connect_string = "mstsc /v:%s" % server.ip
        if server.port:
            connect_string += ":%s" % server.port
        if server.fs:
            connect_string += " /f"
        if server.width:
            connect_string += " /w:%s" % server.width
        if server.height:
            connect_string += " /h:%s" % server.height
        subprocess.Popen(connect_string)

    def clear_form(self):
        self.ui.leDisplayName.setText("")
        self.ui.leIP.setText("")
        self.ui.lePort.setText("")
        self.ui.leWidth.setText("")
        self.ui.leHeight.setText("")
        self.ui.cbFullScreen.setCheckState(QtCore.Qt.CheckState.Unchecked)
    def rem_server(self):
        if self.index == None or self.ui.cbServers.count() <= 0:
            return
        server = self.get_selected_server()
        del self.servers[server.title]
        self.ui.cbServers.removeItem(self.index)
        self.clear_form()

    def save_conf(self):
        self.config = ConfigParser.RawConfigParser()
        for server_name, server in self.servers.iteritems():
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

    def load_server(self, index):
        self.index = index

        server = self.get_selected_server()
        self.ui.leDisplayName.setText(server.title)
        self.ui.leIP.setText(server.ip)
        self.ui.lePort.setText(server.port)
        self.ui.leWidth.setText(server.width)
        self.ui.leHeight.setText(server.height)
        cbChecked = QtCore.Qt.CheckState.Unchecked if server.fs == False else QtCore.Qt.CheckState.Checked
        self.ui.cbFullScreen.setCheckState(cbChecked)

    def get_selected_server(self):
        title = self.ui.cbServers.itemText(self.index)
        return self.servers[title]




def main():
    app = QtGui.QApplication(sys.argv)
    ex = pyRDC()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()