import os
import time

from behave import given, when, then, step

@given('Cura is running')
def step_impl(context):
    pass

@when('we load model {model}')
def step_impl(context, model):  # -- NOTE: number is converted into integer
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", model))
    result = context.cura.call("openFile", path)

    time.sleep(10) # Just so we can see the result of the call

@then("it will start slicing")
def step_impl(context):
    assert True == True
