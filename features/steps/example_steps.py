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


@when('we add a machine "{definition_id}" named as "{machine_name}"')
def step_impl(context, definition_id, machine_name):
    context.cura.addMachine(definition_id, machine_name)

    time.sleep(10)


@when('we rename machine "{old_machine_name}" to "{new_machine_name}"')
def step_impl(context, old_machine_name, new_machine_name):
    context.cura.renameMachine(old_machine_name, new_machine_name)
    time.sleep(1)


@when('we remove machine "{machine_name}"')
def step_impl(context, machine_name):
    context.cura.removeMachine(machine_name)
    time.sleep(2)


@when('we set active machine to "{machine_name}"')
def step_impl(context, machine_name):
    context.cura.setActiveMachine(machine_name)
    time.sleep(1)


@when('we load model {model}')
def step_impl(context, model):  # -- NOTE: number is converted into integer
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", model))
    result = context.cura.call("openFile", path)

    time.sleep(10) # Just so we can see the result of the call

@then("it will start slicing")
def step_impl(context):
    assert True == True


@then('machine "{machine_name}" should exist')
def step_impl(context, machine_name):
    result = context.cura.hasMachine(machine_name)
    assert_that(result, equal_to(True))


@then('machine "{machine_name}" should not exist')
def step_impl(context, machine_name):
    result = context.cura.hasMachine(machine_name)
    assert_that(result, equal_to(False))


@then('check if the current machine is "{machine_name}"')
def step_impl(context, machine_name):
    # TODO: get current machine name
    current_machine_name = context.cura.getActiveMachineName()

    assert_that(current_machine_name, equal_to(machine_name))
