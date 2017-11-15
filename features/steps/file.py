import os
import time

from behave import when, then
from hamcrest import assert_that, equal_to


@when('we load model "{model}"')
def load_model(context, model):  # -- NOTE: number is converted into integer
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", model))
    context.cura.call("openFile", path)

    time.sleep(10)  # Just so we can see the result of the call


@then('we save gcode to "{file_name}"')
def step_save_gcode(context, file_name):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", file_name))
    context.cura.saveGcode(path)
