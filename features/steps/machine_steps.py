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
    time.sleep(5)


@when('we set active extruder to "{extruder_position}"')
def step_impl(context, extruder_position):
    context.cura.setActiveExtruder(extruder_position)
    time.sleep(5)


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


@then('the extruder below is activated')
def step_impl(context):
    actual_extruder_data = context.cura.getActiveExtruder()
    assert context.table, "a table of materials is required"

    for row in context.table:
        for key, value in row.items():
            assert_that(key in actual_extruder_data, "[%s] is not in the extruder data [%s]" % (key, actual_extruder_data))
            assert_that(str(value), equal_to(str(actual_extruder_data[key])),
                        "field [%s] don't match" % key)
