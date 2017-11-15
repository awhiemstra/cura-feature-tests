import time

from behave import given, when, then

@given('we wait for {interval} seconds')
@when('we wait for {interval} seconds')
@then('we wait for {interval} seconds')
def step_wait(context, interval):
    time.sleep(int(interval))
