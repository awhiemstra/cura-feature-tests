import sys
import os
import time

from behave import *

from PyQt5.QtCore import QProcess, QObject
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtDBus import QDBusMessage, QDBusConnection, QDBusReply


class CuraProxy(QObject):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.__executable_path = os.environ.get("CURA_EXECUTABLE", "C:/Program Files/Python35/python.exe")
        self.__process = None

        self.__dbus_service = "nl.ultimaker.cura"

    def start(self):
        if self.__process is not None:
            return

        self.__process = QProcess(self)
        self.__process.setProgram(self.__executable_path)
        self.__process.setArguments(["C:/workspace/repositories/Cura/cura_app.py", "--headless"])
        self.__process.start()
        self.__process.waitForStarted()

        time.sleep(45)  # TODO: This should wait for notification

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

    def addMachine(self, definition_id, machine_name):
        self.call("addMachine", definition_id, machine_name)

    def hasMachine(self, machine_name):
        reply = QDBusReply(self.call("hasMachine", machine_name))
        return reply.value()

    def renameMachine(self, old_machine_name, new_machine_name):
        self.call("renameMachine", old_machine_name, new_machine_name)

    def removeMachine(self, machine_name):
        self.call("removeMachine", machine_name)

    def getActiveMachineName(self):
        reply = QDBusReply(self.call("getActiveMachineName"))
        return reply.value()

    def setActiveMachine(self, machine_name):
        self.call("setActiveMachine", machine_name)


def before_all(context):
    context.qt_app = QGuiApplication(sys.argv)
    context.cura = CuraProxy()


def after_all(context):
    context.cura.stop()


def before_feature(context, feature):
    _removeCuraDirectories()
    context.cura.start()


def after_feature(context, feature):
    context.cura.stop()


def _removeCuraDirectories():
    import platform
    import shutil
    dirs_to_remove = []
    if platform.system().lower() == "windows":
        user_home = os.path.expanduser("~")
        dirs_to_remove = [os.path.join(user_home, "AppData", "Local", "cura"),
                          os.path.join(user_home, "AppData", "Roaming", "cura")]
    # TODO: add code for linux and mac

    for dir_to_remove in dirs_to_remove:
        if os.path.isdir(dir_to_remove):
            shutil.rmtree(dir_to_remove, ignore_errors=True)
            print("Dir [%s] removed" % dir_to_remove)
