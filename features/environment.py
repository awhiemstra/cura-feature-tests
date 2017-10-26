import sys
import os
import time

from PyQt5.QtCore import QProcess, QObject
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtDBus import QDBusMessage, QDBusConnection

from behave import *

class CuraProxy(QObject):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.__executable_path = os.environ["CURA_EXECUTABLE"]
        self.__process = None

        self.__dbus_service = "nl.ultimaker.cura"

    def start(self):
        if self.__process is not None:
            return

        self.__process = QProcess(self)
        self.__process.setProgram(self.__executable_path)
        self.__process.start()
        self.__process.waitForStarted()

        time.sleep(45) # TODO: This should wait for notification

    def stop(self):
        self.call("quit")
        self.__process.waitForFinished()

    def call(self, dbus_method, *args, dbus_object = "/Application", dbus_interface = "nl.ultimaker.cura.Application"):
        message = QDBusMessage.createMethodCall(self.__dbus_service, dbus_object, dbus_interface, dbus_method)
        message.setArguments(args)
        return QDBusConnection.sessionBus().call(message)

    def connectSignal(self, dbus_signal, dbus_object, dbus_interface):
        pass

    def waitForSignal(self, dbus_signal, dbus_object, dbus_interface):
        self.connectSignal(dbus_signal, dbus_object, dbus_interface)

def before_all(context):
    context.qt_app = QGuiApplication(sys.argv)
    context.cura = CuraProxy()

def after_all(context):
    pass

def before_feature(context, feature):
    context.cura.start()

def after_feature(context, feature):
    context.cura.stop()
