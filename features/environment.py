import json
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
        self.__process.setArguments(["--headless"])
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

    def setActiveMaterial(self, material_id):
        self.call("setActiveMaterial", material_id)

    def getActiveMaterial(self):
        return json.loads(self.call("getActiveMaterial").arguments()[0])

    def createMaterial(self, material_id, material_name):
        self.call("createMaterial", material_id, material_name)

    def duplicateMaterial(self, base_material_id, new_id):
        self.call("duplicateMaterial", base_material_id, new_id)

    def hasMaterial(self, material_id):
        return self.call("hasMaterial", material_id).arguments()[0]

    def getMaterial(self, material_id):
        return json.loads(self.call("getMaterial", material_id).arguments()[0])

    def removeMaterial(self, material_id):
        self.call("removeMaterial", material_id)

    def renameMaterial(self, material_id, new_name):
        self.call("renameMaterial", material_id, new_name)

    def importMaterial(self, material_file_path):
        self.call("importMaterial", material_file_path)

    def exportMaterial(self, material_id, material_file_path):
        self.call("exportMaterial", material_id, material_file_path)

    def setActiveExtruder(self, extruder_position):
        self.call("setActiveExtruder", extruder_position)

    def getActiveExtruder(self):
        data = self.call("getActiveExtruder").arguments()[0]
        return json.loads(data)

    def setActiveQuality(self, quality_id):
        self.call("setQualityProfile", quality_id)

    def getActiveQuality(self):
        data = self.call("getActiveQuality").arguments()[0]
        return json.loads(data)

    def saveGcode(self, file_name):
        self.call("saveFile", file_name)

    def slice(self):
        self.call("slice", dbus_object = "/Backend", dbus_interface = "nl.ultimaker.cura.Backend")


def before_all(context):
    context.qt_app = QGuiApplication(sys.argv)
    context.cura = CuraProxy()


def after_all(context):
    context.cura.stop()


def before_feature(context, feature):
    #_removeCuraDirectories()
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
    elif platform.system().lower() == "darwin":
        user_home = os.path.expanduser("~")
        dirs_to_remove = [os.path.join(user_home, "Library", "Application Support", "cura")]
    elif platform.system().lower() == "linux":
        user_home = os.path.expanduser("~")
        dirs_to_remove = [os.path.join(user_home, ".config", "cura"),
                          os.path.join(user_home, ".local", "share", "cura"),
                          os.path.join(user_home, ".cache", "cura"),]

    for dir_to_remove in dirs_to_remove:
        if os.path.isdir(dir_to_remove):
            shutil.rmtree(dir_to_remove, ignore_errors=True)
            print("Dir [%s] removed" % dir_to_remove)
