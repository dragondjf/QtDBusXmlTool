#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtDBus import *
from PyQt5.QtXml import *


DBusError = {
    QDBusError.NoError : "QDBusError is invalid (i.e., the call succeeded)",
    QDBusError.Other   :   "QDBusError contains an error that is one of the well-known ones",
    QDBusError.Failed  :   "The call failed (org.freedesktop.DBus.Error.Failed)",
    QDBusError.NoMemory  :  "Out of memory (org.freedesktop.DBus.Error.NoMemory)",
    QDBusError.ServiceUnknown :   "The called service is not known (org.freedesktop.DBus.Error.ServiceUnknown)",
    QDBusError.NoReply :   "The called method did not reply within the specified timeout (org.freedesktop.DBus.Error.NoReply)",
    QDBusError.BadAddress  :   "The address given is not valid (org.freedesktop.DBus.Error.BadAddress)",
    QDBusError.NotSupported    :   "The call/operation is not supported (org.freedesktop.DBus.Error.NotSupported)",
    QDBusError.LimitsExceeded  :   "The limits allocated to this process/call/connection exceeded the pre-defined values (org.freedesktop.DBus.Error.LimitsExceeded)",
    QDBusError.AccessDenied    :   "The call/operation tried to access a resource it isn't allowed to (org.freedesktop.DBus.Error.AccessDenied)",
    QDBusError.NoServer    :  "Documentation doesn't say what this is for (org.freedesktop.DBus.Error.NoServer)",
    QDBusError.Timeout :  "Documentation doesn't say what this is for or how it's used (org.freedesktop.DBus.Error.Timeout)",
    QDBusError.NoNetwork   :  "Documentation doesn't say what this is for (org.freedesktop.DBus.Error.NoNetwork)",
    QDBusError.AddressInUse    :  "QDBusServer tried to bind to an address that is already in use (org.freedesktop.DBus.Error.AddressInUse)",
    QDBusError.Disconnected    :  "The call/process/message was sent after QDBusConnection disconnected (org.freedesktop.DBus.Error.Disconnected)",
    QDBusError.InvalidArgs :  "The arguments passed to this call/operation are not valid (org.freedesktop.DBus.Error.InvalidArgs)",
    QDBusError.UnknownMethod   :  "The method called was not found in this object/interface with the given parameters (org.freedesktop.DBus.Error.UnknownMethod)",
    QDBusError.TimedOut    :  "Documentation doesn't say... (org.freedesktop.DBus.Error.TimedOut)",
    QDBusError.InvalidSignature    :  "The type signature is not valid or compatible (org.freedesktop.DBus.Error.InvalidSignature)",
    QDBusError.UnknownInterface    :  "The interface is not known in this object (org.freedesktop.DBus.Error.UnknownInterface)",
    QDBusError.UnknownObject   :  "The object path points to an object that does not exist (org.freedesktop.DBus.Error.UnknownObject)",
    QDBusError.UnknownProperty : "The property does not exist in this interface (org.freedesktop.DBus.Error.UnknownProperty)",
    QDBusError.PropertyReadOnly  :  "The property set failed because the property is read-only (org.freedesktop.DBus.Error.PropertyReadOnly)",
    QDBusError.InternalError   :  "An internal error occurred",
    QDBusError.InvalidObjectPath   :  "The object path provided is invalid.",
    QDBusError.InvalidService  :  "The service requested is invalid.",
    QDBusError.InvalidMember   :  "The member is invalid.",
    QDBusError.InvalidInterface :  "The interface is invalid",
}


class DBusToXmlTool(QFrame):
    

    default_service = "com.deepin.menu"
    default_path = "/com/deepin/menu"
    default_interface = "org.freedesktop.DBus.Introspectable"

    default_xml2cpp = "/home/djf/opt/Qt5.4.0/5.4/gcc_64/bin/qdbusxml2cpp"

    unused_interface = [
        u'org.freedesktop.DBus.Introspectable',
        u'org.freedesktop.DBus.Properties',
        u'org.freedesktop.DBus.Peer',
        u'com.deepin.DBus.LifeManager'
    ]

    doctype = """<!DOCTYPE node PUBLIC '-//freedesktop//DTD D-BUS Object Introspection 1.0//EN' 'http://www.freedesktop.org/standards/dbus/1.0/introspect.dtd'>"""

    style = '''
        QFrame#DBusToXmlTool{
            background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:1, fx:0.5, fy:0.5, stop:0 rgba(119, 255, 255, 255), stop:1 rgba(32, 127, 155, 255));
        }
        QLabel{
            background-color: transparent;
        }

        QCheckBox {
            color: black;
        }

        QLineEdit:read-only {
            background: lightgray;
        }
    '''

    def __init__(self, parent=None):
        super(DBusToXmlTool, self).__init__(parent)
        self.setObjectName("DBusToXmlTool")
        self.initUI()
        self.initConnect()

    def initUI(self):
        self.resize(800, 600)
        self.serviceLabel = QLabel("Service Name:")
        self.serviceLineEdit = QLineEdit(self.default_service)

        self.pathLabel = QLabel("Path Name:")
        self.pathLineEdit = QLineEdit(self.default_path)

        self.interfaceLabel = QLabel("Interface Name:")
        self.interfaceLineEdit = QLineEdit(self.default_interface)
        self.interfaceLineEdit.setReadOnly(True)

        self.qdbusxml2cppLabel = QLabel("qdbusxml2cpp path:")
        self.xml2cppLineEdit = QLineEdit(self.default_xml2cpp)
        self.browserButton = QPushButton("...")
        xml2cppLayout = QHBoxLayout()
        xml2cppLayout.addWidget(self.xml2cppLineEdit)
        xml2cppLayout.addWidget(self.browserButton)


        self.interfaceFolderLabel = QLabel("Ouput Interface File Folder:")

        self.folderButton = QPushButton("...")
        self.interfaceFolderLineEdit = QLineEdit(os.getcwd())
        folderLayout = QHBoxLayout()
        folderLayout.addWidget(self.interfaceFolderLineEdit)
        folderLayout.addWidget(self.folderButton)

        

        self.interfaceHNameLabel = QLabel("Ouput Interface File Name:")
        self.interfaceHNameLineEdit = QLineEdit()

        self.interfaceClassNameCheckBox = QCheckBox("Interface Class Name:")
        self.interfaceClassNameCheckBox.setCheckState(Qt.Checked)

        self.interfaceClassNameLineEdit = QLineEdit("Interface")

        self.checkXmlButton = QPushButton("check xml")
        self.checkCppButton = QPushButton("check cpp")
        self.openCurrentFolder = QPushButton("Open Output Folder")
        checkLayout = QVBoxLayout()
        checkLayout.addWidget(self.checkXmlButton)
        checkLayout.addWidget(self.checkCppButton)
        checkLayout.addStretch()
        checkLayout.addWidget(self.openCurrentFolder)

        self.xmlViwer = QTextEdit()
        self.xmlViwer.setAcceptRichText(True)

        self.nameSpaceCheckBox = QCheckBox("NameSpace off")
        self.nameSpaceCheckBox.setCheckState(Qt.Checked)

        self.generateButton = QPushButton("generate")
        self.clearButton = QPushButton("clear")
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.generateButton)
        buttonLayout.addWidget(self.clearButton)

        layout = QGridLayout()

        layout.addWidget(self.serviceLabel, 0, 0)
        layout.addWidget(self.serviceLineEdit, 0, 1)

        layout.addWidget(self.pathLabel, 1, 0)
        layout.addWidget(self.pathLineEdit, 1, 1)

        layout.addWidget(self.interfaceLabel, 2, 0)
        layout.addWidget(self.interfaceLineEdit, 2, 1,)

        layout.addWidget(self.qdbusxml2cppLabel, 3, 0)
        layout.addLayout(xml2cppLayout, 3, 1)

        layout.addWidget(self.interfaceFolderLabel, 4, 0)
        layout.addLayout(folderLayout, 4, 1)

        layout.addWidget(self.interfaceHNameLabel, 5, 0)
        layout.addWidget(self.interfaceHNameLineEdit, 5, 1)

        layout.addWidget(self.interfaceClassNameCheckBox, 6, 0)
        layout.addWidget(self.interfaceClassNameLineEdit, 6, 1)

        layout.addWidget(self.nameSpaceCheckBox, 7, 0)
        layout.addLayout(buttonLayout, 7, 1)

        layout.addLayout(checkLayout, 8, 0, Qt.AlignTop)
        layout.addWidget(self.xmlViwer, 8, 1)

        self.setLayout(layout)

        self.setStyleSheet(self.style)


    def initConnect(self):
        self.generateButton.clicked.connect(self.updateXmlViewer)
        self.clearButton.clicked.connect(self.clearAbandonFiles)
        self.browserButton.clicked.connect(self.changeXml2cppPath)

        self.checkXmlButton.clicked.connect(self.viewXml)
        self.checkCppButton.clicked.connect(self.viewCpp)

        self.interfaceHNameLineEdit.textChanged.connect(self.updateClassNameLineEdit)

    @property
    def xmlPath(self):
        return "%s.xml" % self.interfaceLineEdit.text()\

    @property
    def interface_h(self):
        prefix = self.interfaceHNameLineEdit.text()
        prefix_interface_h = "%s_interface.h" % prefix
        return prefix_interface_h

    @property
    def interface_className(self):
        return self.interfaceClassNameLineEdit.text()

    def updateClassNameLineEdit(self, text):
        self.interfaceClassNameLineEdit.setText(text.capitalize() + "Interface")

    def updateXmlViewer(self):
        service = self.serviceLineEdit.text()
        path = self.pathLineEdit.text()
        interface = self.interfaceLineEdit.text()

        sessionBus = QDBusConnection.sessionBus()
        dbusMessage =  QDBusMessage.createMethodCall(service, path, interface, "Introspect")
        reply = QDBusReply(sessionBus.call(dbusMessage))
        if reply.isValid():
            value = reply.value()
            s = self.getAvaiableInterface(value)
            text = self.doctype + '\n' + s

            with open(self.xmlPath, 'w') as f:
                f.write(text)

            self.xml2cpp()
        else:
            text = "message:    %s \nname:         %s \ndetail:         %s" % (reply.error().message(),
                 reply.error().name(),
                 DBusError[reply.error().type()]
                )
        
        self.xmlViwer.setPlainText(text)

    def changeXml2cppPath(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,
                "QFileDialog.getOpenFileName()", "",
                "All Files (*)", options=options)

        self.xml2cppLineEdit.setText(fileName)

    def getAvaiableInterface(self, value):
        document = QDomDocument()
        document.setContent(value)
        rootElement =  document.documentElement()
        unusedNodes = []
        node = rootElement.firstChild();
        parentNode = node.parentNode()
        while not node.isNull():
            element = node.toElement()
            if element.attribute("name") in self.unused_interface:
                unusedNodes.append(node)
            node = node.nextSibling()
        for node in  unusedNodes:
            parentNode.removeChild(node)

        ss = QByteArray()
        stream = QTextStream(ss)
        parentNode.save(stream, 4)

        return str(ss)

    def xml2cpp(self):
        program = self.xml2cppLineEdit.text()
        isClassNameChecked = self.interfaceClassNameCheckBox.checkState() == Qt.Checked
        isNameSpaceOff = self.nameSpaceCheckBox.checkState() == Qt.Checked

        if isClassNameChecked and isNameSpaceOff:
            QProcess.execute(program, ['-N', '-p', self.interface_h ,'-c', self.interface_className, self.xmlPath])
        elif isClassNameChecked and not isNameSpaceOff:
            QProcess.execute(program, ['-p', self.interface_h ,'-c', self.interface_className, self.xmlPath])
        elif not isClassNameChecked and isNameSpaceOff:
            QProcess.execute(program, ['-N', '-p', self.interface_h , self.xmlPath])
        else:
            QProcess.execute(program, ['-p', self.interface_h , self.xmlPath])

    def viewXml(self):
        if os.path.exists(self.xmlPath):
            with open(self.xmlPath, 'r') as f:
                content = f.read()
            self.xmlViwer.setPlainText(content)

    def viewCpp(self):
        if os.path.exists(self.interface_h):
            with open(self.interface_h, 'r') as f:
                content = f.read()
            self.xmlViwer.setPlainText(content)

    def clearAbandonFiles(self):
        if os.path.exists(self.interface_h):
            QFile(self.interface_h).remove()
        if os.path.exists(self.xmlPath):
            QFile(self.xmlPath).remove()
        self.xmlViwer.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    if not QDBusConnection.sessionBus().isConnected():
        print("Cannot connect to the D-Bus session bus."
                "Please check your system settings and try again.")
        sys.exit(1)

    tool = DBusToXmlTool()
    tool.show()

    exitCode = app.exec_()
    sys.exit(exitCode)
