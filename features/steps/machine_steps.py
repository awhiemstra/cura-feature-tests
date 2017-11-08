import time

from behave import when, then
from hamcrest import assert_that, equal_to


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
