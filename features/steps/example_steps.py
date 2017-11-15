import os
import platform
import time
import shutil

from behave import given, when, then, step
from hamcrest import assert_that, equal_to


@given('clear Cura directories')
def step_impl(context):
    dirs_to_remove = []
    if platform.system().lower() == "windows":
        user_home = os.path.expanduser("~")
        dirs_to_remove = [os.path.join(user_home, "AppData", "Local", "cura"),
                          os.path.join(user_home, "AppData", "Roaming", "cura")]
    # TODO: add code for linux and mac

    for dir_to_remove in dirs_to_remove:
        if os.path.isdir(dir_to_remove):
            shutil.rmtree(dir_to_remove, ignore_errors = True)
            print("Dir [%s] removed" % dir_to_remove)

    time.sleep(2)


@given('Cura is running')
def step_impl(context):
    pass


@then("it will start slicing")
def step_impl(context):
    assert True == True
